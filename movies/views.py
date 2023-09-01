from .serializer import MovieSerializer, UserRegistrationSerializer, UserTokenSeralizer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from .models import Movie, UserInteraction
import random

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        methods=['post'],
        operation_description="Register a new user in the application.",
        responses={201: "Successful response", 400: "Invalid registration"},
    )
    @action(detail=False, methods=['post'])
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    @swagger_auto_schema(
        methods=['post'],
        operation_description="User login.",
        responses={200: "Successful response", 400: "Invalid login"},
    )
    @action(detail=False, methods=['post'])
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                token, created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSeralizer(user)

                if not created:
                    token.delete()
                    token = Token.objects.create(user = user)

                return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Successful Login'
                    }, status=status.HTTP_200_OK)
                
            else:      
                return Response({'error': 'Incorrect password or user name'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Incorrect password or user name'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=['post'],
        operation_description="User logout.",
        responses={201: "Successful response", 400: "Invalid logout"},
    )
    @action(detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):

        user = User.objects.get(username = request.user)
        if user:
            
            token = Token.objects.get(user = user)
            print(token)
            if token:
                token.delete()
                return Response({'message': 'Successful logout'}, status=status.HTTP_200_OK)
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    

class RandomMovieView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        operation_description="Get the detail of a random movie stored in the DB",
        responses={200: "Successful response", 404: "No data stored"},
    )
    @action(detail=False, methods=['get'])
    def get(self, request):
        total_elements = Movie.objects.count()
        if total_elements > 0:
            random_index = random.randint(0, total_elements - 1)
            random_elem = Movie.objects.all()[random_index]
            serializer = MovieSerializer(random_elem)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No elements stored in the database."}, status=status.HTTP_404_NOT_FOUND)

class SortMovieView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        operation_description="Sort all movies and series in the database by name, type, genre or score.",
        responses={200: "Successful response", 400: "Invalid sort field"},
    )
    @action(detail=False, methods=['get'])
    def get(self, request):
        order_by = request.query_params.get('by', None)
        
        if order_by and order_by in [field.name for field in Movie._meta.get_fields()]:
            order_objects = Movie.objects.all().order_by(order_by)
            serializer = MovieSerializer(order_objects, many = True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid sort field"}, status= status.HTTP_400_BAD_REQUEST)

class FilterMovieView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        operation_description="Filter all movies and series in the database by name, type and genre.",
        responses={200: "Successful response", 400: "Invalid filter field"},
    )
    @action(detail=False, methods=['get'])
    def get(self, request):
        name = request.query_params.get('name', None)
        type = request.query_params.get('type', None)
        genre = request.query_params.get('genre', None)

        movies = Movie.objects.all()
        if name:
            movies = movies.filter(name__icontains=name)
        if type:
            movies = movies.filter(type=type)
        if genre:
            movies = movies.filter(genre=genre)
        
        if not name and not type and not genre:
            return Response({"error": "Invalid filter field"}, status=status.HTTP_200_OK)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddVisualizationMovieView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=['patch'],
        operation_description="Protected endpoint. The views of a movie or serie increase by one when the user chooses to mark the movie as watched.",
        responses={200: "Successful response", 404: "Not found", 400: "User already seen this movie", 401: "Unauthorized"},
    )
    @action(detail=False, methods=['patch'])
    def patch(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(username = request.user)
        interaction, flag = UserInteraction.objects.get_or_create(user = user.username, movie = movie)
        if not interaction.visualization:
            movie.visualizations += 1
            interaction.visualization = True
            movie.save()
            interaction.save()
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User already seen this movie'}, status=status.HTTP_400_BAD_REQUEST)

class AddScoreMovieView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        methods=['patch'],
        operation_description="Protected endpoint. A user can rate a movie and its average score is updated.",
        responses={200: "Successful response", 404: "Not found", 400: "User already rated this movie", 400: "Invalid score", 401: "Unauthorized"},
    )
    @action(detail=False, methods=['patch'])
    def patch(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(username = request.user)
        interaction, flag = UserInteraction.objects.get_or_create(user = user.username, movie = movie)
        if not interaction.visualization:
            return Response({'error': 'The user must have seen the movie before to be able to rate it'}, status=status.HTTP_400_BAD_REQUEST)

        if not interaction.score:
            score = request.data.get('score', None)
            if score is None:
                return Response({'error': 'Score field is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if score < 0 or score > 5:
                return Response({'error': 'Score must be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)
            
            total_sum = (movie.qty_score * movie.score) + score
            new_score = round(total_sum / (movie.visualizations), 2)
            movie.score = new_score
            movie.qty_score += 1
            interaction.score = True
            movie.save()
            interaction.save()

            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User already rated this movie'}, status=status.HTTP_400_BAD_REQUEST)
