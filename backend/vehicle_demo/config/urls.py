# config\urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vehicle_demo.users.api.urls', namespace='users_api')),
    path('api/token/', views.obtain_auth_token, name='api-token'),

    # Swagger UI 설정
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Debug toolbar URLs 추가
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
