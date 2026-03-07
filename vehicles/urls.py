from users import urls, views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vehicles import views

router = DefaultRouter()
router.register(r'vehicles', views.VehicleViewSet, basename='vehicle')

urlpatterns = [
    path('', include(router.urls)),
]

