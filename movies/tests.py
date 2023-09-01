from rest_framework.test import APITestCase
from rest_framework import status
from .models import Movie  
from django.contrib.auth.models import User

class MyAPITests(APITestCase):

    def setUp(self):
        Movie.objects.create(name='UP', genre = 'infantil', type = 'movie', score = 3)
        Movie.objects.create(name='OA', genre = 'drama', type = 'serie')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    
    def test_get_random_no_data(self):
        Movie.objects.all().delete()
        response = self.client.get('/api/movies/random')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'No elements stored in the database.')

    def test_get_random(self):
        response = self.client.get('/api/movies/random')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(response.data['id'], 2)
        self.assertIn(response.data['name'], ['UP', 'OA'])
    
    def test_sort_movies_name(self):
        response = self.client.get('/api/movies/sort?by=name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 2)
        self.assertEqual(response.data[0]['name'], 'OA')
        self.assertEqual(response.data[1]['id'], 1)
        self.assertEqual(response.data[1]['name'], 'UP')

    def test_sort_movies_type(self):
        response = self.client.get('/api/movies/sort?by=type')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'UP')
        self.assertEqual(response.data[0]['type'], 'movie')
        self.assertEqual(response.data[1]['id'], 2)
        self.assertEqual(response.data[1]['name'], 'OA')
        self.assertEqual(response.data[1]['type'], 'serie')

    def test_sort_movies_genre(self):
        response = self.client.get('/api/movies/sort?by=genre')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 2)
        self.assertEqual(response.data[0]['name'], 'OA')
        self.assertEqual(response.data[0]['genre'], 'drama')
        self.assertEqual(response.data[1]['id'], 1)
        self.assertEqual(response.data[1]['name'], 'UP')
        self.assertEqual(response.data[1]['genre'], 'infantil')

    def test_sort_movies_score(self):
        response = self.client.get('/api/movies/sort?by=score')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 2)
        self.assertEqual(response.data[0]['name'], 'OA')
        self.assertEqual(response.data[0]['score'], 0.0)
        self.assertEqual(response.data[1]['id'], 1)
        self.assertEqual(response.data[1]['name'], 'UP')
        self.assertEqual(response.data[1]['score'], 3.0)
    
    def test_sort_movies_fail(self):
        response = self.client.get('/api/movies/sort?by=other')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid sort field')
    
    def test_filter_movies_name(self):
        response = self.client.get('/api/movies/filter?name=O')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 2)
        self.assertEqual(response.data[0]['name'], 'OA')
    
    def test_filter_movies_type(self):
        response = self.client.get('/api/movies/filter?type=movie')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'UP')

    def test_filter_movies_genre(self):
        response = self.client.get('/api/movies/filter?genre=infantil')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'UP')
    
    def test_filter_movies_genre_name(self):
        response = self.client.get('/api/movies/filter?genre=infantil&name=U')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'UP')
    
    def test_filter_movies_genre_name_empty(self):
        response = self.client.get('/api/movies/filter?genre=infantil&name=Kill')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
    
    def test_filter_movies_fail(self):
        response = self.client.get('/api/movies/filter?papas=si')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'],'Invalid filter field')
    
    def test_add_visualization_fail_auth(self):
        response = self.client.patch('/api/movies/1/views')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],'Authentication credentials were not provided.')
    
    def test_add_visualization_movie_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/10/views')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Movie not found')

    def test_add_visualization(self):
        movie = Movie.objects.get(id = 1)
        self.assertEqual(movie.visualizations, 0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/1/views')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['visualizations'], 1)
    
    def test_add_visualization_user_once(self):
        movie = Movie.objects.get(id = 1)
        self.assertEqual(movie.visualizations, 0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/1/views')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['visualizations'], 1)
        response = self.client.patch('/api/movies/1/views')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User already seen this movie')
    
    def test_add_score_fail_auth(self):
        response = self.client.patch('/api/movies/2/score')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],'Authentication credentials were not provided.')
    
    def test_add_fail_movie_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/10/score')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Movie not found')
    
    def test_add_score_not_seen_movie(self):
        movie = Movie.objects.get(id = 2)
        self.assertEqual(movie.score, 0.0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        data = {'score': 4.2}
        response = self.client.patch('/api/movies/2/score', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'The user must have seen the movie before to be able to rate it')
    
    def test_add_score_fail_body(self):
        movie = Movie.objects.get(id = 2)
        self.assertEqual(movie.score, 0.0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/2/views')
        data = {'other': 4.2}
        response = self.client.patch('/api/movies/2/score', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Score field is required')

    def test_add_score_incorrect_score(self):
        movie = Movie.objects.get(id = 2)
        self.assertEqual(movie.score, 0.0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/2/views')
        data = {'score': 55}
        response = self.client.patch('/api/movies/2/score', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Score must be between 0 and 5')

    def test_add_score(self):
        movie = Movie.objects.get(id = 2)
        self.assertEqual(movie.score, 0.0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/2/views')
        data = {'score': 4.2}
        response = self.client.patch('/api/movies/2/score', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 4.2)
    
    def test_add_score_user_once(self):
        movie = Movie.objects.get(id = 2)
        self.assertEqual(movie.score, 0.0)
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/movies/2/views')
        data = {'score': 4.2}
        response = self.client.patch('/api/movies/2/score', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 4.2)
        response = self.client.patch('/api/movies/2/score', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User already rated this movie')
