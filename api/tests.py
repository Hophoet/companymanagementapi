from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .serializers import AddNewEmployeeSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from django.shortcuts import reverse
from .models import User

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

   