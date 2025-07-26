import logging
from django.db import transaction
from django.contrib.auth.models import User

from api.eshop.core.singleton import Singleton
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem
from api.eshop.models.dough_type import DoughType
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.ingredient import Ingredient

logger = logging.getLogger(__name__)


class CartService(metaclass=Singleton):
    @staticmethod
    def get_or_create_cart_for_user(user: User) -> Cart:
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            logger.info(f"Cart created for user {user.username} (ID: {cart.id}).")
        else:
            logger.info(f"Retrieved cart for user {user.username} (ID: {cart.id}).")
        return cart

    @staticmethod
    def _check_item_availability(menu_item: MenuItem, dough_type: DoughType, requested_baguette_quantity: int):
        if not menu_item.is_available:
            logger.warning(f"Menu item '{menu_item.name}' is not available (base item unavailable).")
            raise ValueError(f"Menu item '{menu_item.name}' is not available (base item unavailable).")
        if not dough_type.is_available:
            logger.warning(f"Dough type '{dough_type.name}' is not available.")
            raise ValueError(f"Dough type '{dough_type.name}' is not available.")
        
        # Loop through each ingredient that is part of this menu_item's recipe
        for ingredient in menu_item.ingredients.all():  # Access via direct ManyToMany field
            # Apply the rule: "1 unit of each ingredient per 1 unit of product"
            needed_qty_for_this_ingredient = requested_baguette_quantity

            if ingredient._stored_qty < needed_qty_for_this_ingredient:
                logger.warning(f"Ingredient shortage for '{ingredient.name}'. Needed: {needed_qty_for_this_ingredient}, Available: {ingredient._stored_qty}.")
                raise ValueError(f"Not enough '{ingredient.name}' in stock for {menu_item.name}. Needed: {needed_qty_for_this_ingredient}, Available: {ingredient._stored_qty}.")

    @staticmethod
    def add_item_to_cart(
        cart: Cart,
        menu_item_id: int,
        dough_type_id: int,
        quantity: int,
        note: str = None
    ) -> Cart:
        logger.info(f"Attempting to add item {menu_item_id} (dough: {dough_type_id}, qty: {quantity}) to cart {cart.id}.")
        with transaction.atomic():
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
                dough_type = DoughType.objects.get(id=dough_type_id)
            except (MenuItem.DoesNotExist, DoughType.DoesNotExist):
                logger.error(f"Failed to add item: Menu item {menu_item_id} or dough type {dough_type_id} not found.")
                raise ValueError("Menu item or dough type not found.")

            # Availability check (using the corrected method)
            try:
                CartService._check_item_availability(menu_item, dough_type, quantity)
            except ValueError as e:
                logger.error(f"Failed to add item due to availability: {e}")
                raise

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                menu_item=menu_item,
                dough_type=dough_type,
                defaults={'quantity': quantity, 'note': note}
            )
            if not created:
                result_qty = cart_item.quantity + quantity
                logger.info(f"Updated existing cart item {cart_item.id}: quantity from {cart_item.quantity} to {result_qty}.")
                cart_item.quantity += quantity
                cart_item.note = note if note is not None else cart_item.note
                cart_item.save()

        logger.info(f"Item {menu_item.name} (x{quantity}) successfully added/updated in cart {cart.id}.")
        return cart

    @staticmethod
    def update_cart_item_quantity(cart_item_id: int, new_quantity: int, user: User) -> Cart:
        logger.info(f"Attempting to update cart item {cart_item_id} to quantity {new_quantity} for user {user.username}.")
        with transaction.atomic():
            try:
                cart = Cart.objects.get(user=user)
                cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                logger.error(f"Failed to update item: Cart item {cart_item_id} not found for user {user.username}")
                raise ValueError("Cart item not found or does not belong to the user's cart.")

            if new_quantity <= 0:
                logger.info(f"Removing cart item {cart_item.id} (quantity set to 0).")
                cart_item.delete()
            else:
                # Re-check availability for the new total quantity needed
                # (This assumes the check is for the final quantity after update,
                # not just the delta, which is simpler for the given rule).
                try:
                    CartService._check_item_availability(cart_item.menu_item, cart_item.dough_type, new_quantity)
                except ValueError as e:
                    logger.error(f"Failed to update item {cart_item.id} due to availability: {e}")
                    raise  # Re-raise the ValueError

                logger.info(f"Updating cart item {cart_item.id} quantity from {cart_item.quantity} to {new_quantity}.")
                cart_item.quantity = new_quantity
                cart_item.quantity = new_quantity
                cart_item.save()

        logger.info(f"Cart item {cart_item_id} quantity updated successfully for user {user.username}.")
        return cart_item.cart

    @staticmethod
    def remove_cart_item(cart_item_id: int, user: User):
        logger.info(f"Attempting to remove cart item {cart_item_id} for user {user.username}.")
        with transaction.atomic():
            try:
                cart = Cart.objects.get(user=user)
                cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                logger.error(f"Failed to remove item: Cart item {cart_item_id} not found for user {user.username}")
                raise ValueError("Cart item not found or does not belong to the user's cart.")
            cart_item.delete()
            logger.info(f"Cart item {cart_item_id} removed successfully for user {user.username}.")
        return True
