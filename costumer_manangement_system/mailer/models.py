from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Annoncement(models.Model):
    name = models.CharField(max_length=150)
    body = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='announcement', blank=True)
