from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home_page, name="home"),
    path("face/", views.face_page, name="face"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path('profile/', views.profile_page, name='profile'),
    path("logout/", views.logout_page, name="logout"),
    path('voice/', views.voice_page, name='voice'),
    path('media/<str:emotion>/', views.media_page, name='media'),
    path('open_youtube/<str:emotion>/', views.open_youtube, name='open_youtube'),
    path('search_by_title/<str:emotion>/<str:title>/', views.search_by_title, name='search_by_title'),
    path('show_books/<str:emotion>/', views.show_books, name='show_books'),
    path('show_movies/<str:emotion>/', views.show_movies, name='show_movies'),
]