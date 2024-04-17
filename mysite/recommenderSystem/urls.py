from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home_page, name="home"),
    path("face/", views.face_page, name="face"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
]