from django.http import request
from rest_framework import serializers
from .models import Crew, Request

class CrewSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = ['id', 'name', 'description', 'type', 'logo_url', 'owner', 'members', 'country', 'city', 'is_private']
        read_only_fields = ['owner', 'created_at', 'updated_at', 'members']

    def create(self, validated_data):

        logo_url = validated_data.get('logo_url')
        if not logo_url:
            validated_data['logo_url'] = "https://ikkrwtthvkvbeumdgqgw.supabase.co/storage/v1/object/sign/images-doucments/crewnophoto.jpeg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV85ZmE3MzQwMC1kZTc5LTQ5OTQtOWNjZC1mYTVkZWQxZmJiYmYiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJpbWFnZXMtZG91Y21lbnRzL2NyZXdub3Bob3RvLmpwZWciLCJpYXQiOjE3NzI5OTc1MTgsImV4cCI6MjA4ODM1NzUxOH0.M3chCAZIrnDP1lINZx__IuzxLH3INM9MGH8KWty7x2c"
        validated_data['owner'] = self.context['request'].user
        crew = Crew.objects.create(**validated_data)

        crew.members.add(crew.owner) 

        return crew

class RequestCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'crew', 'status']
        read_only_fields = ['status']