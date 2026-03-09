from django.db import models

from kickstanddrfbackend.models import BaseModel

# Create your models here.
class rides(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    route_url = models.URLField(max_length=2000, blank=True, null=True)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='rides')
    crew = models.ForeignKey('crews.Crew', on_delete=models.CASCADE, related_name='rides', blank=True, null=True)

    def __str__(self):
        return self.name