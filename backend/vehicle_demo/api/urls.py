from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleAnalyticsViewSet, RouteOptimizationViewSet, AlertHistoryViewSet

router = DefaultRouter()
router.register(r"vehicle-analytics", VehicleAnalyticsViewSet)
router.register(r"route-optimization", RouteOptimizationViewSet)
router.register(r"alert-history", AlertHistoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
