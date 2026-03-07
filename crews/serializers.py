from django.http import request
from rest_framework import serializers
from .models import Crew

class CrewSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = ['id', 'name', 'description', 'type', 'logo_url', 'owner', 'members', 'country', 'city', 'is_private']
        read_only_fields = ['owner', 'created_at', 'updated_at', 'members']

    def create(self, validated_data):

        crew = Crew.objects.create(**validated_data)
        owner = validated_data.get('owner') or self.context['request'].user
        crew.members.add(owner)  # Add the owner to the members list

        return crew

