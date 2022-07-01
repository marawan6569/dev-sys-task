from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    country_code = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=14, unique=True)
    gender = models.CharField(max_length=6)
    birthdate = models.DateField()
    avatar = models.ImageField(upload_to='avatars/')
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country_code', 'gender', 'birthdate']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Status(models.Model):
    _status_choices = (
        ('inactive', 'inactive'),
        ('active', 'active'),
        ('superuser', 'superuser'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=_status_choices)

    def __str__(self):
        return f'{self.user} => ({self.status})'
