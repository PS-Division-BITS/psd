from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    # allowing email to be used as username
    email = models.EmailField(unique=True)
    # Adding other fields
    # Although these fields are not strictly related to
    # authentication or autherization process, we still decide
    # to store them here so to avoid unnecessary creation of tables
    campus_choices = [
        ('GOA', 'Goa'),
        ('HYD', 'Hyderabad'),
        ('PILANI', 'Pilani'),
    ]

    contact = models.CharField(max_length=10, blank=True, null=True)
    campus = models.CharField(max_length=10, choices=campus_choices)
    cgpa = models.CharField(max_length=6, default="NA")
