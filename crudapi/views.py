from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from rest_framework import status
from .serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_student(student):
    refresh = RefreshToken.for_user(student)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
class StudentApi(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
            stu=Student.objects.get(pk=id)
            serializer=StudentSerializer(stu)
            return Response(serializer.data)
        stu=Student.objects.all()   
        serializer=StudentSerializer(stu,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            # print("save data")
            tokens = get_tokens_for_student(student)

            student.refresh_token = tokens['refresh']
            student.access_token = tokens['access']
            student.save()
            return Response({'msg':'data created !', 'tokens': tokens},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
        
    
    def patch(self,request,pk=None,format=None):
        # token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        id=pk
        stu=Student.objects.get(pk=id)
        serializer=StudentSerializer(stu,data=request.data,partial=True)
        # if token != student.access_token:
        #     return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'partial data updated'})
        return Response(serializer.errors)
    
    def put(self,request,pk=None,format=None):
        id=pk
        stu=Student.objects.get(pk=id)
        serializer=StudentSerializer(stu,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'complete  data updated'})
        return Response(serializer.errors)
    
    def delete(self,request,pk,format=None):
        id=pk
        stu=Student.objects.get(pk=id)
        stu.delete()
        return Response({'msg':"data delete"})