import webbrowser
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .utility import *
from .forms import CreateUserForm


def home_page(request):
    return render(request, 'home.html')


def media_page(request, emotion):
    context = {'emotion': emotion}
    return render(request, 'media.html', context)


def open_youtube(request, emotion):
    webbrowser.open(f"https://www.youtube.com/results?search_query={emotion}+songs")
    return redirect('media', emotion)


def search_by_title(request, emotion, title):
    webbrowser.open(f"https://www.google.com/search?q={title}")
    return redirect('media', emotion)


def show_books(request, emotion):
    genres = get_genres_by_emotion(emotion)
    books = get_ten_books(genres)
    titles = books['Title']
    context = {'titles': titles, 'emotion': emotion}
    return render(request, 'show_recommendations.html', context)


def show_movies(request, emotion):
    genres = get_genres_by_emotion(emotion)
    movies = get_ten_movies(genres)
    titles = movies['movie_name']
    context = {'titles': titles, 'emotion': emotion}
    return render(request, 'show_recommendations.html', context)


def voice_page(request):
    emotion = "happy"
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        emotion = emotion_by_voice(audio_file)
        return redirect('media', emotion)

    context = {'emotion': emotion}
    return render(request, 'voice.html', context)


def face_page(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        emotion = emotion_by_face(image_file.read())
        return JsonResponse({'emotion': emotion})

    context = {'emotion': 's'}
    return render(request, 'face.html', context)


def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def profile_page(request):
    context = {'user': request.user}
    return render(request, 'profile.html', context)