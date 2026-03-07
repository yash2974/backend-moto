from django import db
from django.db import models
from django.contrib.auth.models import User
from kickstanddrfbackend.models import BaseModel

# Create your models here.
class Vehicle(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True, blank=True, null=True, db_index=True) #optional license plate field
    image_url = models.URLField(max_length=200, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    service_interval = models.IntegerField(null=True, blank=True)  # in KMs
    specs = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.license_plate or 'No License Plate'})"  