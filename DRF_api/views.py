from django.shortcuts import render
# parsing data from the client
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
# API definition for task
from .serializers import UserSerializer, MyFileSerializer, FileUploadSerializer
# Task model
from .models import Task, User
# Create your views here.
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd 
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

class UsersView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
        operation_summary='Return the user data'
    )
    def get(self, request, *args, **krgs):
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='Add a new user'
    )
    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise Response({'error': str(e)},  status=status.HTTP_400_BAD_REQUEST)
    
class DeleteView(GenericAPIView):

    @swagger_auto_schema(
        operation_summary='Delete a user by name'
    )
    def delete(self, request, user):
        try:
            user = User.objects.filter(pk = user)
            if not user:
                return Response({"Fail":"Name is not in Database"}, status=status.HTTP_200_OK)
            else:   
                user.delete()

                return Response({"result":"user delete"}, status=status.HTTP_200_OK)
        except Exception as e:
            raise Response({'error': str(e)},  status=status.HTTP_400_BAD_REQUEST)
        
class MyFileView(GenericAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = FileUploadSerializer

    @swagger_auto_schema(
        operation_summary='Upload CSV file'
    )
    def post(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            # csv_file = pd.read_csv(file_serializer.data["file"])
            file = file_serializer.validated_data['file']
            reader = pd.read_csv(file)
            for idx, row in reader.iterrows():
                user_database = User(
                    name=row["Name"],
                    age=row["Age"]
                )
                user_database.save()
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        else:
            raise Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupView(GenericAPIView):
    serializer_class = UserSerializer

    def get_first_letter(self, letter):
        return letter[0].lower() 
    
    # 使用函数
    @swagger_auto_schema(
        operation_summary='Find the average of each grop of users'
    )
    def get(self, request, *args, **kwargs):
        user_data = User.objects.all()
        users = []
        for user in user_data:
            users.append({"name":user.name, "age":user.age})
        df_users  = pd.DataFrame(users)
        groupby_mean_res = df_users.set_index('name').groupby(self.get_first_letter).mean().to_json()
        
        return Response(groupby_mean_res)

class ClearDBView(GenericAPIView):

    @swagger_auto_schema(
        operation_summary='Clear DB'
    )
    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.all()
            user.delete()
            return Response({"Clear DB":"success"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("error message:%s", e)
            raise Response(Exception, status=status.HTTP_400_BAD_REQUEST)
    
