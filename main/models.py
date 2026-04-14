from django.db import models

# Create your models here.

<<<<<<< HEAD
=======

>>>>>>> 782cb0e (Initial commit)
class Contact(models.Model):
    subject = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
<<<<<<< HEAD
    description = models.TextField()
=======
    description = models.TextField()


class Booking(models.Model):
    movie = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField(default=1)
>>>>>>> 782cb0e (Initial commit)
