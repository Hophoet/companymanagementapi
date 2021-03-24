from rest_framework import serializers
from django.contrib.auth.models import User

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
            'username',
            'email',
            'profil',
            'date_joined',
            'last_login'
        )



class AddNewTaskSerializer(serializers.Serializer):
    """ add new task end point serializer """
    title = serializers.CharField()
    description = serializers.CharField()
    employee_id = serializers.IntegerField()
    deadline = serializers.DateTimeField()