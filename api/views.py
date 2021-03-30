from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import (AddNewEmployeeSerializer, 
                            UpdateEmployeeSerializer, 
                            DeleteEmployeeSerializer, 
                            UserSerializer,
                            AddNewTaskSerializer,
                            UpdateTaskSerializer,
                            DeleteTaskSerializer,
                            TaskSerializer
                            )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from .models import Profil, Task

class GetAuthenticatedUser(APIView):
    """ authenticated user getting view """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ post request method """
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=HTTP_200_OK)

class UserIsAnAdminView(APIView):
    """ employee getting by admin view """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ post request method """
        user = request.user
        is_staff = user.is_staff
        
        return Response(data={'is_admin': is_staff}, status=HTTP_200_OK)

class GetEmployeesView(APIView):
    """ employee getting by admin view """
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        """ post request method """
        employees = User.objects.filter(profil__isnull=False)
        serializer = UserSerializer(employees, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

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

        profil.salary = salary
        profil.picture = picture
        profil.save()
        return Response(data=serializer.data, status=HTTP_200_OK)

class DeleteEmployeeView(APIView):
    """ employee deleting management by admin view """
    permission_classes = (IsAdminUser,)
    serializer_class = DeleteEmployeeSerializer

    def delete(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        #
        employee_id = serializer.data.get('employee_id')
        try:
            employee = User.objects.get(id=employee_id)
        except ObjectDoesNotExist as error:
            return Response(data={'text':'employee not exists'}, status=HTTP_400_BAD_REQUEST)
         
        try:
            Profil.objects.get(user=employee)
        except ObjectDoesNotExist as error:
            return Response(data={'text':f'this user{employee} it not an employee'}, status=HTTP_400_BAD_REQUEST)

        employee.delete()
        return Response(data={'text':f'employee({employee}) deleted successfully'}, status=HTTP_200_OK)



class GetTasksView(APIView):
    """ tasks getting by admin view """
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        """ post request method """
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

#
class AddNewTaskView(APIView):
    """ tasks adding management by admin view """
    permission_classes = (IsAdminUser,)
    serializer_class = AddNewTaskSerializer

    def post(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        #
        employee_id = serializer.data.get('employee_id')
        title = serializer.data.get('title')
        description = request.data.get('description')
        deadline = request.data.get('deadline')
        try:
            employee = User.objects.get(id=employee_id, is_staff=False)
        except ObjectDoesNotExist as error:
            return Response(data={'text':'employee not exists'}, status=HTTP_400_BAD_REQUEST)
        Task.objects.create(employee=employee, title=title, description=description, deadline=deadline)

        return Response(data=serializer.data, status=HTTP_200_OK)


class UpdateTaskView(APIView):
    """ task updating management by admin view """
    permission_classes = (IsAdminUser,)
    serializer_class = UpdateTaskSerializer

    def put(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        #
        task_id = serializer.data.get('task_id')
        title = serializer.data.get('title')
        description = serializer.data.get('description')
        deadline = request.data.get('deadline')
        try:
            task = Task.objects.get(id=task_id)
        except ObjectDoesNotExist as error:
            return Response(data={'text':'task not exists'}, status=HTTP_400_BAD_REQUEST)

        
        task.title = title
        task.description = description
        task.deadline = deadline
        task.save()
        return Response(data=serializer.data, status=HTTP_200_OK)

class DeleteTaskView(APIView):
    """ task deleting management by admin view """
    permission_classes = (IsAdminUser,)
    serializer_class = DeleteTaskSerializer

    def delete(self, request, *args, **kwargs):
        """ post request method """
        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        #
        task_id = serializer.data.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except ObjectDoesNotExist as error:
            return Response(data={'text':'task not exists'}, status=HTTP_400_BAD_REQUEST)

        task.delete()
        return Response(data={'text':f'task({task.title}) deleted successfully'}, status=HTTP_200_OK)


class GetEmployeeTasks(APIView):
    """ tasks getting by admin view """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ post request method """
        tasks = Task.objects.filter(employee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)



class UserProfilView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


