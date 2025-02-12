from rest_framework import serializers
from .models import VehicleAnalytics, RouteOptimization, AlertHistory

class VehicleAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAnalytics
        fields = "__all__"

class RouteOptimizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteOptimization
        fields = "__all__"

class AlertHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertHistory
        fields = "__all__"
