from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.helloWorld, name='world')
]
