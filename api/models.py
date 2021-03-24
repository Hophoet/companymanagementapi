from django.db import models
from django.contrib.auth import get_user_model

# User model, this model represent the employee and the admins
User = get_user_model()


# Employee task, represent a task that can be assigned to the employee by the admin
class Task(models.Model):
    """ Employee tasks model """
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    title = models.CharField(max_length=100)
    description = models.TextField()
    dealine = models.DateTimeField()


# Profil model represent the additinal information for the employee
class Profil(models.Model):
    """ Employee Profile, for additional informations for the user """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    picture = models.ImageField()
    salary = models.IntegerField()

    def __str__(self):
        return f'salary: {self.salary}'



