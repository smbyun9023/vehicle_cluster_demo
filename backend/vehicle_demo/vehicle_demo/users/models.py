from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djongo import models as djongo_models  # Djongo를 사용할 때 필요


class User(AbstractUser):
    """
    Default custom user model for vehicle_demo.
    """
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view."""
        return reverse("users:detail", kwargs={"username": self.username})


### MongoDB 모델 (Vehicle Sensor Data) ###
class GPSData(djongo_models.Model):
    latitude = djongo_models.FloatField()
    longitude = djongo_models.FloatField()

    class Meta:
        abstract = True  # EmbeddedModelField 사용 시 필요


class VehicleSensorData(djongo_models.Model):
    vehicle_id = djongo_models.CharField(max_length=50)
    timestamp = djongo_models.DateTimeField()
    gps = djongo_models.EmbeddedModelField(model_container=GPSData)
    speed = djongo_models.FloatField()
    temperature = djongo_models.FloatField()
    image_url = djongo_models.URLField()
    raw_data = djongo_models.JSONField(null=True, blank=True)

    objects = djongo_models.DjongoManager()  # Djongo 전용 매니저 사용


### PostgreSQL 모델 (Django 기본 ORM) ###
class VehicleAnalytics(models.Model):
    vehicle_id = models.CharField(max_length=50)
    anal_time = models.DateTimeField()
    avg_speed = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    distance = models.FloatField(null=True, blank=True)
    anom_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle_id} - {self.anal_time}"


class RouteOptimization(models.Model):
    vehicle_id = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_loc = models.JSONField()  # 좌표 저장
    end_loc = models.JSONField()
    optm_route = models.JSONField()  # 최적 경로 데이터

    def __str__(self):
        return f"{self.vehicle_id} - {self.start_time} to {self.end_time}"


class AlertHistory(models.Model):
    vehicle_id = models.CharField(max_length=50)
    alert_time = models.DateTimeField()
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[("SENT", "SENT"), ("FAILED", "FAILED")])

    def __str__(self):
        return f"{self.vehicle_id} - {self.alert_time} ({self.alert_type})"
