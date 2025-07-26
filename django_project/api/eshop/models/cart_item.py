from django.db import models
from api.eshop.models.cart import Cart
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.dough_type import DoughType
from decimal import Decimal


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    dough_type = models.ForeignKey(DoughType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'eshop_app'
        unique_together = ('cart', 'menu_item', 'dough_type')  # A cart can have only one unique combo of menu item and dough type
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} ({self.dough_type.name}) in Cart {self.cart.id}"

    @property
    def price(self):
        # Calculate price per unit (MenuItem base price + DoughType extra price)
        return self.menu_item.base_price + self.dough_type.extra_price
