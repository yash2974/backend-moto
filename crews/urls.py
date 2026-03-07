from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crews import views

router = DefaultRouter()
router.register(r'crews', views.CrewViewSet, basename='crew')
router.register(r'my-crews', views.OwnerCrewViewSet, basename='owner-crew')

urlpatterns = [
    path('', include(router.urls)),
]
