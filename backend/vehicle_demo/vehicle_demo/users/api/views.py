from rest_framework import status, viewsets
from rest_framework.response import Response
from vehicle_demo.users.models import VehicleSensorData, VehicleAnalytics, RouteOptimization, AlertHistory
from .serializers import VehicleSensorDataSerializer, VehicleAnalyticsSerializer, RouteOptimizationSerializer, AlertHistorySerializer

# 차량 센서 데이터 뷰셋
class VehicleSensorDataViewSet(viewsets.ModelViewSet):
    queryset = VehicleSensorData.objects.all()
    serializer_class = VehicleSensorDataSerializer

# 차량 분석 데이터 뷰셋
class VehicleAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = VehicleAnalytics.objects.all()
    serializer_class = VehicleAnalyticsSerializer

# 경로 최적화 데이터 뷰셋
class RouteOptimizationViewSet(viewsets.ModelViewSet):
    queryset = RouteOptimization.objects.all()
    serializer_class = RouteOptimizationSerializer

# 알림 기록 데이터 뷰셋
class AlertHistoryViewSet(viewsets.ModelViewSet):
    queryset = AlertHistory.objects.all()
    serializer_class = AlertHistorySerializer
