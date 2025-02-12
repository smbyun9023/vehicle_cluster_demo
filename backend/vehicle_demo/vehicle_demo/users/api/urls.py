#users\api\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleSensorDataViewSet, VehicleAnalyticsViewSet, RouteOptimizationViewSet, AlertHistoryViewSet

# DRF Router 설정
router = DefaultRouter()
router.register(r"vehicle-sensor-data", VehicleSensorDataViewSet, basename="vehiclesensordata")
router.register(r"vehicle-analytics", VehicleAnalyticsViewSet, basename="vehicleanalytics")
router.register(r"route-optimization", RouteOptimizationViewSet, basename="routeoptimization")
router.register(r"alert-history", AlertHistoryViewSet, basename="alerthistory")

app_name = "users_api"  # namespace 사용을 위한 app_name 추가

urlpatterns = [
    path("", include(router.urls)),  # API 엔드포인트 자동 등록
]
