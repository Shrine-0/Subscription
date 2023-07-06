from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .serializers import SignUpSerializer,UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
def register(request):
    data =request.data
    
    user = SignUpSerializer(data=data)
    
    if user.is_valid():
        if not User.objects.filter(username = data['email']).exists():
            
            user = User.objects.create(
                username = data['email'],
                password= make_password(data['password']),
                email= data['email'],
                first_name=data['first_name'],
                last_name = data['last_name'],
            )
            user.save()
            
            return Response({'Details':f'User with email {data["email"]} registered successfully'},status = status.HTTP_201_CREATED)
            
        else:
            return Response({'Error':f'User with name {data["username"]} already exists'},status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    
    user.username = data["username"]
    user.email = data["email"]
    user.first_name = data["first_name"]
    user.last_name= data["last_name"]
    
    if data["password"] != "":
        user.password = data["password"]
    user.save() 
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)
    