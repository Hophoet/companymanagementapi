from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from .serializers import AddNewEmployeeSerializer, UpdateEmployeeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from .models import User, Profil


#
class AddNewEmployeeView(APIView):
    """ employee adding management by admin view """
    permission_classes = (IsAdminUser,)
    serializer_class = AddNewEmployeeSerializer

    def post(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        #
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        salary = serializer.data.get('salary')
        picture = request.data.get('picture')
        employee = User.objects.create(username=username, password=password)
        profil = Profil.objects.create(user=employee, salary=salary, picture=picture)

        return Response(data=serializer.data, status=HTTP_200_OK)

        


class UpdateEmployeeView(APIView):
    """ employee updating management by admin view """
    permission_classes = (IsAdminUser,)
    serializer_class = UpdateEmployeeSerializer

    def put(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        #
        employee_id = serializer.data.get('employee_id')
        username = serializer.data.get('username')
        salary = serializer.data.get('salary')
        picture = request.data.get('picture')
        try:
            employee = User.objects.get(id=employee_id)
        except ObjectDoesNotExist as error:
            return Response(data={'text':'employee not exists'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            profil = Profil.objects.get(user=employee)
        except ObjectDoesNotExist as error:
            return Response(data={'text':'this user it not an employee'}, status=HTTP_400_BAD_REQUEST)
        try: 
            employee.username = username
            employee.save()
        except IntegrityError as error:
            return Response(data={'text':'username already exists'}, status=HTTP_400_BAD_REQUEST)

        profil.username = username
        profil.salary = salary
        profil.picture = picture
        profil.save()

        return Response(data=serializer.data, status=HTTP_200_OK)
