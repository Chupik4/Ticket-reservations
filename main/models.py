from django.db import models

# Create your models here.

class Contact(models.Model):
    subject = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()