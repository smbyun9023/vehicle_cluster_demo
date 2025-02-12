from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vehicle_demo.users.api.views import VehicleSensorDataViewSet, VehicleAnalyticsViewSet, RouteOptimizationViewSet, AlertHistoryViewSet

router = DefaultRouter()
router.register(r'vehicle-sensors', VehicleSensorDataViewSet)
router.register(r'vehicle-analytics', VehicleAnalyticsViewSet)
router.register(r'route-optimization', RouteOptimizationViewSet)
router.register(r'alert-history', AlertHistoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
