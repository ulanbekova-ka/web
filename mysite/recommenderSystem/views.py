import webbrowser
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .emotion_detection import emotion_by_voice, emotion_by_face
from .forms import CreateUserForm


def home_page(request):
    return render(request, 'home.html')


def media_page(request, emotion):
    context = {'emotion': emotion}
    return render(request, 'media.html', context)


def open_youtube(request, emotion):
    webbrowser.open(f"https://www.youtube.com/results?search_query={emotion}+songs")
    return redirect('media', emotion)


def find_books(request, emotion):
    webbrowser.open(f"https://www.google.com/search?q={emotion}+books+to+read")
    return redirect('media', emotion)


def find_movies(request, emotion):
    webbrowser.open(f"https://www.google.com/search?q=top+{emotion}+movies")
    return redirect('media', emotion)


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