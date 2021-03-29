from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('is-admin/', views.UserIsAnAdminView.as_view(), name='is_admin'),
    path('employees', views.GetEmployeesView.as_view(), name='get_employees'),
    path('employees/add', views.AddNewEmployeeView.as_view(), name='add_employee'),
    path('employees/update', views.UpdateEmployeeView.as_view(), name='update_employee'),
    path('employees/delete', views.DeleteEmployeeView.as_view(), name='delete_employee'),

    path('tasks', views.GetTasksView.as_view(), name='get_tasks'),
    path('tasks/add', views.AddNewTaskView.as_view(), name='add_task'),
    path('tasks/update', views.UpdateTaskView.as_view(), name='update_task'),
    path('tasks/delete', views.DeleteTaskView.as_view(), name='delete_task'),
    
    path('profil/<int:pk>', views.UserProfilView.as_view(), name='user_profil')
]
