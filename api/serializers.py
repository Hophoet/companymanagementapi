from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class AddNewEmployeeSerializer(serializers.Serializer):
    """ add new employee end point serializer """
    username = serializers.CharField()
    password = serializers.CharField()
    salary = serializers.IntegerField()
    picture = serializers.ImageField() 


class UpdateEmployeeSerializer(serializers.Serializer):
    """ update employee end point serializer """
    employee_id = serializers.IntegerField()
    username = serializers.CharField()
    salary = serializers.IntegerField()
    picture = serializers.ImageField() 



class DeleteEmployeeSerializer(serializers.Serializer):
    """ delete employee end point serializer """
    employee_id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    """ user model serializer """
    profil = serializers.StringRelatedField()
    class Meta:
        """ comment model serializer Meta class """
        model = User
        fields = (
            'id',
            'username',
            'email',
            'profil',
            'date_joined',
            'last_login',
            'is_staff',
            'auth_token'
        )

class TaskSerializer(serializers.ModelSerializer):
    """ task model serializer """
    employee = serializers.StringRelatedField()
    class Meta:
        """ task model serializer Meta class """
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'deadline',
            'employee'
        )


class AddNewTaskSerializer(serializers.Serializer):
    """ add new task end point serializer """
    title = serializers.CharField()
    description = serializers.CharField()
    employee_id = serializers.IntegerField()
    deadline = serializers.DateTimeField()



class UpdateTaskSerializer(serializers.Serializer):
    """ update task end point serializer """
    task_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    deadline = serializers.DateTimeField() 




class DeleteTaskSerializer(serializers.Serializer):
    """ delete task end point serializer """
    task_id = serializers.IntegerField()
