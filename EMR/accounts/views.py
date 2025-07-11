from django.shortcuts import render
from accounts.serializers import LoginSerializer, RegisterUserSerializer, PlanSerializer, CoverageSerializer, ChangePasswordSerializer, UpdateUserProfileSerializer
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from accounts.models import Plans, Coverage, User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from accounts.permissions import IsSuperuser

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

class LoginView(GenericAPIView):
    authentication_classes= [TokenAuthentication]
    serializer_class = LoginSerializer
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data 
        serializer = self.serializer_class(data= data, context = {'request' : request})
        if serializer.is_valid():
            print(serializer)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user =authenticate(request, username= email, password= password)
            if user is not None:
                token, created = Token.objects.get_or_create(user= user)
                display_picture_url = user.display_picture.url if user.display_picture else None
                return Response({
                    'data' : {'token' : token.key, 'is_staff' : user.is_staff, 'is_superuser' : user.is_superuser, 'display' : display_picture_url, 'full_name': user.full_name}
                }, status=status.HTTP_200_OK)
            else: 
                return Response({
                    'error': 'Invalid credentials. Please try again.'
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'error': 'Login failed.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response ({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class PlansViewset(ModelViewSet):
    queryset = Plans.objects.all()
    serializer_class = PlanSerializer
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

class CoverageViewset(ModelViewSet):
    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

class ChangePasswordView(APIView):

    serializer_class = ChangePasswordSerializer
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data.get('old_password')
        password1 = serializer.validated_data.get('password')
        password2 = serializer.validated_data.get('password1')


        if not user.check_password(old_password):
            return Response({"old_password": "Old password is wrong."}, status=status.HTTP_400_BAD_REQUEST)


        user.set_password(password1)
        user.save()

        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
    
class UpdateProfile(APIView):
    serializer_class = UpdateUserProfileSerializer
    authentication_classes = [ TokenAuthentication ]
    permission_classes = [ IsAuthenticated ]

    def put (self, request):
        user = request.user
        edit_user = User.objects.get(email= user.email)
        serializer = UpdateUserProfileSerializer(edit_user, data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)