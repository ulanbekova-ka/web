from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CopingPreferenceForm(forms.Form):
    initial_emotion = forms.ChoiceField(
        choices=(
            ('angry', 'Angry'),
            ('disgust', 'Disgust'),
            ('fear', 'Fear'),
            ('happy', 'Happy'),
            ('sad', 'Sad'),
            ('surprise', 'Surprise'),
            ('neutral', 'Neutral'),
        )
    )
    coping_emotion = forms.ChoiceField(
        choices=(
            ('angry', 'Angry'),
            ('disgust', 'Disgust'),
            ('fear', 'Fear'),
            ('happy', 'Happy'),
            ('sad', 'Sad'),
            ('surprise', 'Surprise'),
            ('neutral', 'Neutral'),
        )
    )

