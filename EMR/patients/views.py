from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.

def helloWorld(request):
    return Response({
        'data' : 'hello, world'
    }) 
