from django.db import models

class DoughType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    extra_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Dough Type"
        verbose_name_plural = "Dough Types"
        ordering = ['name']

    def __str__(self):
        availability_status = "Available" if self.is_available else "Unavailable"
        return f"{self.name} ({availability_status})"
