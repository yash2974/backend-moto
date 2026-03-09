from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from crews.models import Crew, Request
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

    @action(detail=True, methods=["get"])
    def requests(self, request, pk=None):
        crew = self.get_object()
        requests = crew.join_requests.select_related('user').filter(status='pending').order_by('-created_at')
        data = [
            {
                "id": req.id,
                "user": req.user.username,
                "image_url": req.user.profile.image_url if hasattr(req.user, 'profile') else None,
                "status": req.status,
                "created_at": req.created_at,
                "modified_at": req.updated_at
            }
            for req in requests
        ]
        return Response(data, status=200)

    @action(detail=True, methods=["post"], url_path='requests/(?P<request_id>[^/.]+)/(?P<action>approve|reject)')
    def process_request(self, request, pk=None, request_id=None, action=None):
        crew = self.get_object()
        try:
            req = Request.objects.select_related('user').get(id=request_id, crew=crew)
        except Request.DoesNotExist:
            return Response({"message": "Request not found"}, status=404)

        if req.status != 'pending':
            return Response({"message": "Request already processed"}, status=400)

        if action == 'approve':
            req.status = 'approved'
            crew.members.add(req.user)
            message = "Request approved"
        elif action == 'reject':
            req.status = 'rejected'
            message = "Request rejected"
        req.save()
        return Response({"message": message}, status=200)


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
        if crew.members.filter(id=user.id).exists() or crew.owner == user:
            return Response({"message": "Already a member"}, status=404)
        if crew.is_private in ["Invite Only"]:
            request_obj, created = Request.objects.get_or_create(
                user=user,
                crew=crew,
                defaults={"status": "pending"}
            )
            if not created:
                return Response({"message": "Request already sent"}, status=404)

            return Response({"message": "Request sent"}, status=200)
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