from django.db import models

class VehicleAnalytics(models.Model):
    vehicle_id = models.CharField(max_length=50)
    anal_time = models.DateTimeField()
    avg_speed = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    distance = models.FloatField(null=True, blank=True)
    anom_flag = models.BooleanField(default=False)
    adtn_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle_id} - {self.anal_time}"


class RouteOptimization(models.Model):
    vehicle_id = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_loc = models.JSONField()
    end_loc = models.JSONField()
    optm_route = models.JSONField()

    def __str__(self):
        return f"{self.vehicle_id} - {self.start_time} to {self.end_time}"


class AlertHistory(models.Model):
    vehicle_id = models.CharField(max_length=50)
    alert_time = models.DateTimeField()
    alert_type = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.vehicle_id} - {self.alert_type}"
