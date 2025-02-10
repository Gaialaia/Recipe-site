from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    STATUS = (
        ('amateur', 'amateur'),
        ('chef', 'chef'),
        ('seeker', 'seeker'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField(help_text='Few words about yourself', max_length=300, default='', blank=True)
    avatar = models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return self.username