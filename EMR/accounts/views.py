from django.shortcuts import render
from accounts.serializers import UserRegistrationPlanSerializer, LoginSerializer, HospitalRegistrationSerializer, RegisterUserSerializer, PlanSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from accounts.models import Plans

# Create your views here.

class RegisterUser(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data= data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            return Response({
                'Status' : 'Successful',
                'data' : user,
                'message' : f'Account successfully created for {user}'  
            }, status=status.HTTP_201_CREATED)

        return Response({
            'Status' : 'Unsuccessful',
            'data' : serializer.errors,
            'message' : f'An error occured!!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class HospitalRegisterView(GenericAPIView):
    serializer_class = HospitalRegistrationSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data= data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'data' : data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message' : 'An error occurred while creating user',
            'data' : data
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data 
        serializer = self.serializer_class(data= data, context = {'request' : request})
        serializer.is_valid(raise_exception=True)
        return Response({
            'data' : serializer.data,
        }, status=status.HTTP_200_OK)
    

class PlansViewset(ModelViewSet):
    queryset = Plans.objects.all()
    serializer_class = PlanSerializer