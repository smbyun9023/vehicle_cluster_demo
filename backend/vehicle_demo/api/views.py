from rest_framework import viewsets
from .models import VehicleAnalytics, RouteOptimization, AlertHistory
from .serializers import VehicleAnalyticsSerializer, RouteOptimizationSerializer, AlertHistorySerializer

class VehicleAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = VehicleAnalytics.objects.all()
    serializer_class = VehicleAnalyticsSerializer

class RouteOptimizationViewSet(viewsets.ModelViewSet):
    queryset = RouteOptimization.objects.all()
    serializer_class = RouteOptimizationSerializer

class AlertHistoryViewSet(viewsets.ModelViewSet):
    queryset = AlertHistory.objects.all()
    serializer_class = AlertHistorySerializer
