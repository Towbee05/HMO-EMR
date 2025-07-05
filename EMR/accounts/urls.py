from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

routers = DefaultRouter()
routers.register(r'', views.PlansViewset, basename='plans')

urlpatterns = [
    path('accounts/register/', views.RegisterUser.as_view(), name='register_user'),
    path('accounts/register/hospital/', views.HospitalRegisterView.as_view(), name='register_hospital'),
    path('accounts/login/', views.LoginView.as_view(), name='login_user'),
    path('plans/', include(routers.urls))
]

 