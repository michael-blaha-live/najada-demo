from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    _stored_qty = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'eshop_app'
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Qty: {self._stored_qty})"

    @property
    def stored_qty(self):
        """
        Public getter for stored_qty.
        """
        return self._stored_qty

    @property
    def is_available(self):
        """
        Determines if the ingredient is available based on its stored quantity.
        """
        return self._stored_qty > 0
