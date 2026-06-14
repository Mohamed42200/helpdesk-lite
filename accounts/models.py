from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYEE = 'employee', 'Employee'
        AGENT = 'agent', 'Agent'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )

    def is_employee(self):
        return self.role == self.Role.EMPLOYEE

    def is_agent(self):
        return self.role == self.Role.AGENT

    def is_admin_user(self):
        return self.role == self.Role.ADMIN
