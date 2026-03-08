from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"