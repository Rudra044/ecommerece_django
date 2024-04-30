from django.db import models
from user.models import User
from product.models import Product


class Order(models.Model):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUS = (
        (PENDING, 'PENDING'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (COMPLETED, 'COMPLETED'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    quantity = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=15, choices=STATUS, default='PENDING')

