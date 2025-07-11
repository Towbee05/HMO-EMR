from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as authtoken_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/patients/', include('patients.urls')),
    path('api/v1/hospitals/', include('hospitals.urls')),
    path('api/v1/authtoken/', authtoken_views.obtain_auth_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)