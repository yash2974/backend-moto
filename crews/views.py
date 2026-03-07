from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from crews.models import Crew
from crews.serializers import CrewSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

# Create your views here.
class OwnerCrewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CrewSerializer

    def get_queryset(self):
        return Crew.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CrewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CrewSerializer

    def get_queryset(self):
        user = self.request.user
        return Crew.objects.filter(
            Q(is_private__in=['Public', 'Invite Only']) |
            Q(owner=user) |
            Q(members=user)
        ).distinct()
    
    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        crew = self.get_object()
        user = request.user

        if crew.members.filter(id=user.id).exists():
            return Response({"message": "Already a member"}, status=400)

        crew.members.add(user)
        return Response({"message": "Joined crew"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def leave(self, request, pk=None):
        crew = self.get_object()
        user = request.user

        if not crew.members.filter(id=user.id).exists():
            return Response({"message": "Not a member"}, status=400)

        if crew.owner == user:
            return Response({"message": "Owner cannot leave crew"}, status=400)

        crew.members.remove(user)
        return Response({"message": "Left crew"}, status=status.HTTP_200_OK)