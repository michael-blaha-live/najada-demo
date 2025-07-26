import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.eshop.models.dough_type import DoughType
from api.eshop.models.payment_type import PaymentType
from api.eshop.models.ingredient import Ingredient
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem
from api.eshop.tests.factories import (
    UserFactory, DoughTypeFactory, IngredientFactory,
    PaymentTypeFactory, MenuItemFactory, CartFactory, CartItemFactory
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()  # Use factory to create user
    api_client.force_authenticate(user=user)
    return api_client, user


# --- Simplified fixtures using factories ---
@pytest.fixture
def create_dough_type(db):
    def _create_dough_type(name=None, extra_price=0, is_available=True):
        if name is None:  # Use factory's sequence for uniqueness if name not provided
            return DoughTypeFactory(extra_price=extra_price, is_available=is_available)
        return DoughTypeFactory(name=name, extra_price=extra_price, is_available=is_available)
    return _create_dough_type


@pytest.fixture
def create_payment_type(db):
    def _create_payment_type(name=None):
        if name is None:
            return PaymentTypeFactory()
        return PaymentTypeFactory(name=name)
    return _create_payment_type


@pytest.fixture
def create_ingredient(db):
    def _create_ingredient(name=None, quantity=100):
        if name is None:
            return IngredientFactory(_stored_qty=quantity)
        return IngredientFactory(name=name, _stored_qty=quantity)
    return _create_ingredient


@pytest.fixture
def create_menu_item(db):
    def _create_menu_item(name=None, base_price=50.00, ingredients: list = None):  # ingredients is list of Ingredient instances
        if name is None:
            name = f'MenuItem {factory.Sequence(lambda n: n).evaluate(None, None)}'  # noqa
        
        menu_item = MenuItemFactory(name=name, base_price=base_price)
        if ingredients:
            menu_item.ingredients.set(ingredients)  # Add existing instances to M2M
        return menu_item
    return _create_menu_item


@pytest.fixture
def create_cart_with_items(db, authenticated_client, create_menu_item, create_dough_type):
    user = authenticated_client[1]
    
    def _create_cart_with_items(user_obj: User, items_data: list):
        cart = CartFactory(user=user_obj)  # Create cart for the specific user
        for item_data in items_data:
            # Ensure menu_item and dough_type are actual model instances passed or created
            menu_item_instance = item_data.get('menu_item_instance') or MenuItemFactory(
                name=item_data['menu_item_name'],
                base_price=item_data['base_price'],
                ingredients=[IngredientFactory(name=ing_name) for ing_name in item_data['ingredients']]  # Creates unique ingredients for menu item
            )
            dough_type_instance = item_data.get('dough_type_instance') or DoughTypeFactory(
                name=item_data['dough_type_name'],
                extra_price=item_data['extra_price']
            )
            CartItemFactory(
                cart=cart,
                menu_item=menu_item_instance,
                dough_type=dough_type_instance,
                quantity=item_data['quantity'],
                note=item_data.get('note', '')
            )
        return cart
    return _create_cart_with_items


# --- Add other factories as direct fixtures for convenience in tests (optional) ---
@pytest.fixture
def user_factory(db):
    return UserFactory


@pytest.fixture
def dough_type_factory(db):
    return DoughTypeFactory


@pytest.fixture
def ingredient_factory(db):
    return IngredientFactory


@pytest.fixture
def menu_item_factory(db):
    return MenuItemFactory


@pytest.fixture
def payment_type_factory(db):
    return PaymentTypeFactory


@pytest.fixture
def cart_factory(db):
    return CartFactory


@pytest.fixture
def cart_item_factory(db):
    return CartItemFactory
