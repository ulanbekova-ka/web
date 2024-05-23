from django.db import models
from django.contrib.auth.models import User


class CopingPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_emotion = models.CharField(max_length=20)
    coping_emotion = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
