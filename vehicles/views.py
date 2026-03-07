from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import vehicles
from vehicles.serializers import VehicleSerializer
from .models import Vehicle

# Create your views here.
class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer

    def get_queryset(self):
        user = self.request.user
        return Vehicle.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    