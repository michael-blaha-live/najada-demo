import logging
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth.models import User

from api.eshop.core.singleton import Singleton
from api.eshop.models.order import Order
from api.eshop.models.order_item import OrderItem
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem
from api.eshop.models.payment_type import PaymentType
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.dough_type import DoughType
from api.eshop.models.ingredient import Ingredient
from api.eshop.services.cart import CartService

logger = logging.getLogger(__name__)


class OrderService(metaclass=Singleton):
    @staticmethod
    def place_order(cart_id: int, payment_type_id: int, user: User) -> Order:
        logger.info(f"Attempting to place order for user {user.username} from cart {cart_id} with payment type {payment_type_id}.")
        with transaction.atomic():
            try:
                cart = Cart.objects.get(id=cart_id, user=user)
                logger.debug(f"Cart {cart.id} retrieved for user {user.username}.")
            except Cart.DoesNotExist:
                logger.error(f"Cart {cart_id} not found or does not belong to user {user.username}.")
                raise ValueError("Cart not found or does not belong to the user.")

            if not cart.items.exists():
                logger.warning(f"Order placement failed: Cart {cart.id} is empty for user {user.username}.")
                raise ValueError("Cart is empty.")

            try:
                payment_type = PaymentType.objects.get(id=payment_type_id)
            except PaymentType.DoesNotExist:
                logger.debug(f"Payment type id {payment_type_id} retrieved for order.")
                raise ValueError("Payment type not found.")

            # Pre-calculate totals from cart for order
            total_price = cart.total_price
            vat_amount = cart.vat
            price_without_vat = cart.wo_vat_price
            logger.debug(f"Order totals calculated: Total={total_price}, VAT={vat_amount}, WoVAT={price_without_vat}.")

            # --- CRITICAL: Final Availability Check & Stock Deduction ---
            # Iterate through cart items and try to deduct stock
            logger.info(f"Starting final availability check and stock deduction for cart {cart.id}.")
            for cart_item in cart.items.all():
                # Re-check individual item availability from scratch at order time
                # This raises ValueError if stock is insufficient
                logger.debug(f"Checking availability for cart item {cart_item.id} (menu_item: {cart_item.menu_item.name}, quantity: {cart_item.quantity}).")
                try:
                    CartService._check_item_availability(
                        cart_item.menu_item,
                        cart_item.dough_type,
                        cart_item.quantity
                    )
                    logger.debug(f"Availability confirmed for cart item {cart_item.id}.")
                except ValueError as e:
                    logger.error(f"Availability check failed for cart item {cart_item.id}: {e}")
                    raise  # Re-raise the ValueError, which will trigger atomic rollback

                # Deduct stock after confirming availability
                # Assuming 1 unit of ingredient per 1 product, check each ingredient
                logger.debug(f"Deducting stock for menu item {cart_item.menu_item.name} (qty: {cart_item.quantity}).")
                for ingredient_needed in cart_item.menu_item.ingredients.all():
                    needed_qty_for_this_ingredient = cart_item.quantity

                    # Use select_for_update to lock rows and prevent race conditions during deduction
                    # And update _stored_qty directly
                    ingredient = Ingredient.objects.select_for_update().get(id=ingredient_needed.id)
                    ingredient._stored_qty -= needed_qty_for_this_ingredient
                    ingredient.save()
                    logger.info(f"Deducted {needed_qty_for_this_ingredient} of '{ingredient.name}'. Old stock: original_qty, New stock: {ingredient._stored_qty}.")

            # Create the Order
            order = Order.objects.create(
                user=user,
                payment_type=payment_type,
                total_price=total_price,
                price_without_vat=price_without_vat,
                vat_amount=vat_amount,
                status='Created'
            )
            logger.info(f"Order {order.id} created (status: {order.status}) for user {user.username}.")
            # Create OrderItems as snapshots
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    menu_item_snapshot=cart_item.menu_item,
                    dough_type_snapshot=cart_item.dough_type,
                    menu_item_name_at_order=cart_item.menu_item.name,
                    dough_type_name_at_order=cart_item.dough_type.name,
                    unit_price_at_order=cart_item.price,  # Unit price calculated on CartItem model
                    quantity=cart_item.quantity,
                    note=cart_item.note
                )
                logger.debug(f"OrderItem created for {cart_item.menu_item.name} (x{cart_item.quantity}) in Order {order.id}.")

            # Clear the cart after successful order placement
            cart.items.all().delete()
            logger.info(f"Cart {cart.id} cleared for user {user.username} after successful order placement.")
            # Optional: You might want to delete the cart itself if it's no longer needed
            # cart.delete()  # Or just leave it as an empty cart

        return order

    @staticmethod
    def get_user_orders(user: User) -> QuerySet[Order]:
        logger.info(f"Retrieving all orders for user { user.username}.",)
        orders = Order.objects.filter(user=user)
        logger.debug(f"Found {orders.count()} orders for user {user.username}.")
        return orders

    @staticmethod
    def get_order_by_id(order_id: int, user: User) -> Order | None:
        logger.info(f"Attempting to retrieve order {order_id} for user {user.username}.")
        try:
            order = Order.objects.get(id=order_id, user=user)
            logger.debug(f"Order {order.id} retrieved for user {user.username}.")
            return order
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found or does not belong to user {user.username}.")
            return None
