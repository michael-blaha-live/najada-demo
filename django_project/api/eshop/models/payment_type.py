from django.db import models


class PaymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "cash", "credit card"

    class Meta:
        app_label = 'eshop_app'
        verbose_name = "Payment Type"
        verbose_name_plural = "Payment Types"
        ordering = ['name']  # Order by name for consistent retrieval

    def __str__(self):
        return self.name
