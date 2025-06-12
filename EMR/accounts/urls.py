from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('register/hospital/', views.HospitalRegisterView.as_view(), name='register_hospital'),
    path('login/', views.LoginView.as_view(), name='login_user')
]

 