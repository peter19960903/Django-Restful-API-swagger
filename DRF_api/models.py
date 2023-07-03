from django.db import models


# Create your models here.
class Task(models.Model):
    #title
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) #description
    completed = models.BooleanField(default=False)
    #completed
    created_at = models.DateTimeField(auto_now_add=True) #created_at

    def __str__(self):
        #return the task title
        return self.title
    
class User(models.Model):
    name = models.CharField(max_length=100, primary_key=True) 
    age = models.PositiveIntegerField()


class MyFile(models.Model):
    
    file = models.FileField(upload_to="files")

    class Meta:
        verbose_name_plural = 'MyFiles'
    