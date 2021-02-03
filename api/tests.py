from datetime import datetime
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from .serializers import AddNewEmployeeSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from django.shortcuts import reverse
from .models import User, Profil, Task
from PIL import Image
import io

# employees management tests
class EmployeeTestCase(APITestCase):
    """ employee management test case """
    def setUp(self):
        """ base setup values """
        self.api_client = APIClient()
        self.get_employees_url = reverse('api:get_employees')
        self.add_employee_url = reverse('api:add_employee')
        self.update_employee_url = reverse('api:update_employee')
        self.delete_employee_url = reverse('api:delete_employee')
        

    def test_add_new_employee_with_incomplete_data(self):
        """ test the new employee with incompleted request data
            (request) -> 400"""
        user = User.objects.create( username='test user', password='jkld', is_staff=True)
        self.api_client.force_authenticate(user=user)
        data = {'username':'lay', 'password':''}
        response = self.api_client.post(self.add_employee_url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST) 

    def test_add_new_employee_by_not_admin_user(self):
        """ test the new employee saving by not admin authenticated user 
            (request) -> 403"""
        user = User.objects.create( username='test user', password='jkld')
        self.api_client.force_authenticate(user=user)
        data = {'username':'lay', 'password':''}
        response = self.api_client.post(self.add_employee_url, data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN) 


    def generate_photo_file(self):
        """ image file generator """
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_add_new_employee(self):
        """ test the new employee saving with valid data
        (request) -> 200 """
        user = User.objects.create(is_staff=True, username='test user', password='jkld')
        self.api_client.force_authenticate(user=user)
        image = self.generate_photo_file()

        data = {
            'username':'lay', 
            'password':'kjksdfklj',
            'salary':300,
            'picture':image
            
        }
        response = self.api_client.post(self.add_employee_url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)


    def test_get_employees(self):
        """ test the employees avaialble getting 
        (request) -> 200 """
        user = User.objects.create(is_staff=True, username='test user', password='jkld')

        employees_before_employee_created = User.objects.filter(is_staff=False).count()
        #create new employee
        User.objects.create(username='test employee', password='password')

        self.api_client.force_authenticate(user=user)
        response = self.api_client.get(self.get_employees_url)
        employees_after_user_created = User.objects.filter(is_staff=False).count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(employees_after_user_created, employees_before_employee_created + 1)


    def test_delete_employee_with_wrong_employee_id(self):
        """ test employee delete with wrong empoyee id 
        (request) -> 400 as response status code """
        #admin
        user = User.objects.create(is_staff=True, username='admin', password='password')
        self.api_client.force_authenticate(user=user)
        data = {
            'employee_id':user.id + 10
        }
        response = self.api_client.delete(self.delete_employee_url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


    def test_delete_admin_as_employee(self):
        """ test delete admin as employee 
        (request) -> 400 as response status code """
        #admin
        admin = User.objects.create(is_staff=True, username='admin', password='password')
        self.api_client.force_authenticate(user=admin)
        data = {
            'employee_id':admin.id
        }
        response = self.api_client.delete(self.delete_employee_url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_delete_employee_with_success(self):
        """ test done delete employee
        (request) -> 2OO as response status code """
        #admin
        admin = User.objects.create(is_staff=True, username='admin', password='password')
        #employee
        employee = User.objects.create(is_staff=False, username='employee', password='password')
        Profil.objects.create(user=employee, salary=400)
        #employees counts after a new added employee
        employees_count_before_employee_deleted = User.objects.filter(is_staff=False).count()
        self.api_client.force_authenticate(user=admin)
        data = {
            'employee_id':employee.id
        }
        response = self.api_client.delete(self.delete_employee_url, data)
        employees_count_after_employee_added = User.objects.filter(is_staff=False).count()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(employees_count_before_employee_deleted, employees_count_after_employee_added + 1)
        


    def test_employee_update_with_wrong_employee_id(self):
        """ test the employee update with a wrong employee to update id
        (request) -> 400 as response status code(BAD REQUEST) """
        #add employee
        employee = User.objects.create(is_staff=False, username='employee', password='password') #auth
        user = User.objects.create(is_staff=True, username='admin', password='password')
        self.api_client.force_authenticate(user=user)
        #add employee
        data = {
            'username':'lay', 
            'employee_id':employee.id + 10,
            'salary':300,
            'picture':self.generate_photo_file()
        }        
        response = self.api_client.put(self.update_employee_url, data)
        self.assertEqual(response.status_code, 400)




# tasks management tests
class TaskTestCase(APITestCase):
    """ task management test case """
    def setUp(self):
        """ base setup values """
        self.api_client = APIClient()
        self.add_task_url = reverse('api:add_task')
        self.update_task_url = reverse('api:update_task')
        self.delete_task_url = reverse('api:delete_task')
        

    
    def test_add_new_task_with_invalid_employee_id(self):
        """ test the new task to an invalid employee id  
            (request) -> 400"""
        user = User.objects.create( username='test user', password='jkld', is_staff=True)
        #employee
        employee = User.objects.create( username='employee', password='jkld', is_staff=False)
        self.api_client.force_authenticate(user=user)
        data = {
            'employee_id':employee.id+10, 
            'title':'Github workflow',
            'description':'Setup the fastapi api project workflow',
            'deadline':datetime.now()
            
        }
        response = self.api_client.post(self.add_task_url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST) 



    def test_successfull_task_adding(self):
        """ test a valid task adding
            (request) -> 200"""
        user = User.objects.create( username='test user', password='jkld', is_staff=True)
        #employee
        employee = User.objects.create( username='employee', password='jkld', is_staff=False)
        self.api_client.force_authenticate(user=user)
        data = {
            'employee_id':employee.id, 
            'title':'Github workflow',
            'description':'Setup the fastapi api project workflow',
            'deadline':datetime.now()
            
        }
        response = self.api_client.post(self.add_task_url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)


    def test_task_update_with_wrong_task_id(self):
        """ test the task update with a wrong task to update id
        (request) -> 400 as response status code(BAD REQUEST) """
        #add employee, task
        employee = User.objects.create(is_staff=False, username='employee', password='password') #auth
        task = Task.objects.create(employee=employee, title='test task', description='test task description', dealine='2021-03-12 12:34:00')

        #auth
        user = User.objects.create(is_staff=True, username='admin', password='password')
        self.api_client.force_authenticate(user=user)
        #update task
        data = {
            'title':'test task updated', 
            'task_id':task.id + 10,
            'description':'test task description updated',
            'deadline':datetime.now()
        }        
        response = self.api_client.put(self.update_task_url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


    def test_task_update(self):
        """ test valid task update
        (request) -> 200 as response status code(BAD REQUEST) """
        #add employee, task
        employee = User.objects.create(is_staff=False, username='employee', password='password') #auth
        task = Task.objects.create(employee=employee, title='test task', description='test task description', dealine='2021-03-12 12:34:00')

        #auth
        user = User.objects.create(is_staff=True, username='admin', password='password')
        self.api_client.force_authenticate(user=user)
        #update task
        data = {
            'title':'test task updated', 
            'task_id':task.id,
            'description':'test task description updated',
            'deadline':datetime.now()
        }        
        response = self.api_client.put(self.update_task_url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Task.objects.all().count(), 1)