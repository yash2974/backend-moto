import re

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        default_image = "https://ikkrwtthvkvbeumdgqgw.supabase.co/storage/v1/object/sign/images-doucments/noImage.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV85ZmE3MzQwMC1kZTc5LTQ5OTQtOWNjZC1mYTVkZWQxZmJiYmYiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJpbWFnZXMtZG91Y21lbnRzL25vSW1hZ2UucG5nIiwiaWF0IjoxNzcyOTkxNzM4LCJleHAiOjIwODgzNTE3Mzh9.ZEiBtlfsjxO6Eg1bZDPY1YH497wRCiDlcQjEEC_ozx4"
        image_url = self.context.get("image_url", default_image)
        Profile.objects.create(user=user, image_url=image_url)
        return user   

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'image_url']
        read_only_fields = ['date_joined', 'email']
    
    def to_representation(self, instance):
        """Read image_url from the related Profile model"""
        representation = super().to_representation(instance)
        if hasattr(instance, 'profile') and instance.profile:
            representation['image_url'] = instance.profile.image_url
        else:
            representation['image_url'] = None
        return representation
    
    def update(self, instance, validated_data):
        """Handle updating image_url in the Profile model"""
        image_url = validated_data.pop('image_url', None)
        instance = super().update(instance, validated_data)
        
        if image_url is not None:
            profile, created = Profile.objects.get_or_create(user=instance)
            profile.image_url = image_url
            profile.save()
        
        return instance
        
