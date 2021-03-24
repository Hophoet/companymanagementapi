from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('employees/add', views.AddNewEmployeeView.as_view(), name='add_employee'),
    path('employees/update', views.UpdateEmployeeView.as_view(), name='update_employee')
]
