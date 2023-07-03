from rest_framework import routers,serializers,viewsets
from .models import Task, User, MyFile

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at']

class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

#用這個讀取不了csv 
class MyFileSerializer(serializers.ModelSerializer):
     class Meta:
        model = MyFile
        fields = "__all__"