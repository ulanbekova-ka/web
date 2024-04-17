from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home_page, name="home"),
    path("face/", views.face_page, name="face"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path('voice/', views.voice_page, name='voice'),
    path('media/<str:emotion>/', views.media_page, name='media'),
    path('open_youtube/<str:emotion>/', views.open_youtube, name='open_youtube'),
    path('find_books/<str:emotion>/', views.find_books, name='find_books'),
    path('find_movies/<str:emotion>/', views.find_movies, name='find_movies'),
]