from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.movie_list, name='home'),  # Root URL
    path('movies/', views.movie_list, name='movie_list'),
    path("search/",views.search,name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='booking/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('my-tickets/', views.user_tickets, name='user_tickets'),
    path('movies/<int:movie_id>/', views.screenings, name='screenings'),
    path('screenings/<int:screening_id>/', views.seats, name='select_seats'),
    path('booking/<int:seat_id>/', views.booking, name='book_tickets')
]
