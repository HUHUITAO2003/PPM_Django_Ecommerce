from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    codice_fiscale = models.CharField(max_length=16)
    telefono = models.CharField(max_length=20)