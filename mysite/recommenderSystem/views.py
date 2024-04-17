from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .emotion_detection import emotion_by_voice
from .forms import CreateUserForm


def home_page(request):
    return render(request, 'home.html')


def media_page(request):
    return render(request, 'media.html')


def voice_page(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        emotion = emotion_by_voice(audio_file)
        return redirect('media')
    else:
        return render(request, 'voice.html')


def face_page(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        print(image_file)
        return redirect('media')
    return render(request, 'face.html')


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
