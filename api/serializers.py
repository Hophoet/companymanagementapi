from rest_framework import serializers


class AddNewEmployeeSerializer(serializers.Serializer):
    """ add new employee end point serializer """
    username = serializers.CharField()
    password = serializers.CharField()
    salary = serializers.IntegerField()
    picture = serializers.ImageField() 

