from expenses import serializers
from expenses.models import Expense
from vehicles.models import Vehicle
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


# Create your views here.
class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(owner=user)

    def perform_create(self, serializer):
        vehicle_id = self.request.data.get('vehicle')
        if not vehicle_id:
            raise ValidationError("Vehicle license plate is required.")
        
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id, owner=self.request.user)
        except Vehicle.DoesNotExist:
            raise ValidationError("Vehicle not found or does not belong to the user.")
        
        serializer.save(owner=self.request.user, vehicle=vehicle)