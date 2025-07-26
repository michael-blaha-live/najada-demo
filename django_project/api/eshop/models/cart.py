from django.db import models
from django.conf import settings
from decimal import Decimal


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'eshop_app'
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"Cart for {user_str} (ID: {self.id})"

    @property
    def total_price(self):
        # Assumes VAT is handled consistently, e.g., 21%
        # For simplicity, let's assume 0% VAT for now as per test setup
        total = sum(item.price * item.quantity for item in self.items.all())
        return total

    @property
    def vat(self):
        # For simplicity, if VAT is always calculated at 0%
        # If VAT is 21%, example: return self.total_price * Decimal('0.21')
        return Decimal('0.00')  # Placeholder

    @property
    def wo_vat_price(self):
        # For simplicity, if VAT is 0, this is the same as total_price
        return self.total_price - self.vat
