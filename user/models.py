from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLES = (
        (1, 'Buyer'),
        (2, 'Seller'),
    )
    role = models.SmallIntegerField(choices=ROLES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

class Link(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='link_user')
    isUsed = models.BooleanField(default=False)
    token = models.CharField(max_length=5000, null=True)
    expired_time = models.DateTimeField(null=True)