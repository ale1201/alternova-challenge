from django.urls import path
from .views import LogoutView, AddScoreMovieView, LoginView, UserRegistrationView, RandomMovieView, SortMovieView, FilterMovieView, AddVisualizationMovieView


urlpatterns = [
    path('registration', UserRegistrationView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('random', RandomMovieView.as_view()),
    path('sort', SortMovieView.as_view()),
    path('filter', FilterMovieView.as_view()),
    path('<int:id>/views', AddVisualizationMovieView.as_view(), name='movies'),
    path('<int:id>/score', AddScoreMovieView.as_view(), name='movies'),
]