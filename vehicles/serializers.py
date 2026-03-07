from vehicles.models import Vehicle
from rest_framework import serializers

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ["owner", "created_at", "updated_at"]

    # todo validate year, make, model, and vin number and specs json