from django.db import models
from django.contrib.auth.models import User
from kickstanddrfbackend.models import BaseModel

# Create your models here.
class Crew(BaseModel):

    class CrewType(models.TextChoices):
        RACING = 'Sports'
        ADVENTURE = 'Adventure'
        CRUISING = 'Cruising'
        OFFROAD = 'Offroad'

    class IsPrivate(models.TextChoices):
        PUBLIC = 'Public'
        PRIVATE = 'Private'
        INVITE_ONLY = 'Invite Only'

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=CrewType.choices, default=CrewType.RACING)
    logo_url = models.URLField(max_length=1000, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crews')
    members = models.ManyToManyField(User, related_name='crew_memberships', blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    is_private = models.CharField(max_length=20, choices=IsPrivate.choices, default=IsPrivate.PUBLIC)

    def __str__(self):
        return self.name
