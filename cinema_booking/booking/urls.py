from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.movies, name='home'),  # Root URL
    path('movies/', views.movies, name='movies'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('my-tickets/', views.user_tickets, name='user_tickets'),
    path('movies/<int:movie_id>/', views.screenings, name='screenings'),
    path('screenings/<int:screening_id>/', views.seats, name='select_seats'),
    path('booking/<int:seat_id>/', views.booking, name='book_tickets')
]
