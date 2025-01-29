from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    employee = models.BooleanField(default=False)
    #Ein Integer Array um IDs von Projekten zu speichern
    active_projects = models.JSONField(default=dict)
    description = models.CharField(max_length=150)
    member_since = models.DateTimeField(default=timezone.now)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    files = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        # Ensure the default structure for 'files'
        self.files.setdefault("id", [])
        super().save(*args, **kwargs)

"""

{
"id": []
}

"""


