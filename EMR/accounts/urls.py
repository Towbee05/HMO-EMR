from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

plan_routers = DefaultRouter()
plan_routers.register(r'', views.PlansViewset, basename='plans')

coverage_routers = DefaultRouter()
coverage_routers.register(r'', views.CoverageViewset, basename='coverage')

urlpatterns = [
    path('accounts/register/', views.RegisterUser.as_view(), name='register_user'),
    path('accounts/register/hospital/', views.HospitalRegisterView.as_view(), name='register_hospital'),
    path('accounts/changepassword/', views.ChangePasswordView.as_view(), name='change_password'),
    path('accounts/login/', views.LoginView.as_view(), name='login_user'),
    path('plans/', include(plan_routers.urls)),
    path('coverage/', include(coverage_routers.urls)),
]

 