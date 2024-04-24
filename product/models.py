from django.db import models
from user.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()

