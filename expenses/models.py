from django.utils import timezone

from django.db import models

from kickstanddrfbackend.models import BaseModel

# Create your models here.
class Expense(BaseModel):

    class Category(models.TextChoices):
        FUEL = "Fuel"
        MAINTENANCE = "Maintenance"
        REPAIR = "Repair"
        INSURANCE = "Insurance"
        OTHER = "Other"
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="expenses")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20, choices=Category.choices)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"