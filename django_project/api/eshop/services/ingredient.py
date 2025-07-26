import logging
from api.eshop.core.singleton import Singleton
from api.eshop.models.ingredient import Ingredient
from django.db.models import QuerySet

logger = logging.getLogger(__name__)


class IngredientService(metaclass=Singleton):
    @staticmethod
    def get_all_ingredients() -> QuerySet[Ingredient]:
        return Ingredient.objects.all()

    @staticmethod
    def get_ingredient_by_id(ingredient_id: int) -> Ingredient | None:
        try:
            return Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            logging.info(f"Ingredient with id {ingredient_id} not found.")
            return None

    @staticmethod
    def update_stock(ingredient: Ingredient, quantity_change: int) -> Ingredient:
        # This method would typically be called by OrderService, etc.
        ingredient._stored_qty += quantity_change  # Directly modify the internal field
        ingredient.save()
        logger.info(f"Ingredient {ingredient.name} quantity changed to {ingredient._stored_qty}")
        return ingredient
