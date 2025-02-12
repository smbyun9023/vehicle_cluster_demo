from rest_framework import serializers
from vehicle_demo.users.models import VehicleSensorData, VehicleAnalytics, RouteOptimization, AlertHistory


# 차량 센서 데이터 직렬화
class VehicleSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleSensorData
        fields = '__all__'

# 차량 분석 데이터 직렬화
class VehicleAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAnalytics
        fields = '__all__'

# 경로 최적화 데이터 직렬화
class RouteOptimizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteOptimization
        fields = '__all__'

# 알림 기록 데이터 직렬화
class AlertHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertHistory
        fields = '__all__'
