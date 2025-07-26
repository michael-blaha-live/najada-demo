from django.db import models
from api.eshop.models.ingredient import Ingredient


class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items')

    class Meta:
        app_label = 'eshop_app'
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        # Assumes 1 unit of each ingredient is needed for 1 unit of product (rule from zadani)
        # So we check if each *required* ingredient is available at all (stored_qty > 0)
        for ingredient in self.ingredients.all():
            if not ingredient.is_available:  # Checks ingredient._stored_qty > 0
                return False
        return True
