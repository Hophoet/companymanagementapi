from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from .serializers import AddNewEmployeeSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from django.shortcuts import reverse
from .models import User
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