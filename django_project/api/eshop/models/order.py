from django.db import models
from django.conf import settings
from api.eshop.models.payment_type import PaymentType
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Preparing Food', 'Preparing Food'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Created')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_without_vat = models.DecimalField(max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'eshop_app'
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} for {self.user.username} ({self.status})"
