from django.db import models
from api.eshop.models.order import Order
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.dough_type import DoughType
from decimal import Decimal


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    # Snapshots of the menu item and dough type details at the time of order
    menu_item_snapshot = models.ForeignKey(MenuItem, on_delete=models.PROTECT)  # PROTECT to keep historical reference
    dough_type_snapshot = models.ForeignKey(DoughType, on_delete=models.PROTECT)  # PROTECT to keep historical reference

    menu_item_name_at_order = models.CharField(max_length=255)
    dough_type_name_at_order = models.CharField(max_length=100)
    unit_price_at_order = models.DecimalField(max_digits=8, decimal_places=2)  # Base + extra dough price

    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'eshop_app'
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        # Optional: unique_together for order_item, menu_item_snapshot, dough_type_snapshot if multiple of same item are not allowed

    def __str__(self):
        return f"{self.quantity}x {self.menu_item_name_at_order} ({self.dough_type_name_at_order}) in Order {self.order.id}"
