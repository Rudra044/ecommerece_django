from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    ROLES = (
        (1, 'Buyer'),
        (2, 'Seller'),
    )
    role = models.SmallIntegerField(choices=ROLES)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Link(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='link_user')
    isUsed = models.BooleanField(default=False)
    token = models.CharField(max_length=5000, null=True)
    expired_time = models.DateTimeField(null=True)