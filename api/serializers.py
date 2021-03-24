from rest_framework import serializers


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