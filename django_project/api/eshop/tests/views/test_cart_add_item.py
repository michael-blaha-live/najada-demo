import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.dough_type import DoughType
from api.eshop.models.ingredient import Ingredient
from api.eshop.serializers.cart import CartSerializer
from api.eshop.serializers.cart_item_detail import CartItemDetailSerializer
from api.eshop.serializers.cart_item_request import CartItemRequestSerializer
from api.eshop.tests.factories import IngredientFactory, DoughTypeFactory, MenuItemFactory, CartFactory, CartItemFactory


@pytest.mark.django_db
class TestCartAddItem:

    def test_add_new_valid_item_to_empty_cart(self, authenticated_client, create_menu_item, create_dough_type, create_ingredient):
        user = authenticated_client[1]
        Cart.objects.filter(user=user).delete()

        ingredient_cheese = IngredientFactory(name="Flour for Bagel", _stored_qty=10)
        menu_item = MenuItemFactory(name="Bagel", base_price=50.00, ingredients=[ingredient_cheese])
        dough_type = DoughTypeFactory(name="soft dough", extra_price=5.00, is_available=True)

        data = {
            "menu_item_id": menu_item.id,
            "dough_type_id": dough_type.id,
            "quantity": 1,
            "note": "Extra crispy"
        }

        response = authenticated_client[0].post('/api/eshop/cart/items/', data, format='json')

        assert response.status_code == 200
        response_json = response.json()
        assert response_json['id'] == Cart.objects.get(user=user).id
        assert len(response_json['items']) == 1
        assert response_json['items'][0]['quantity'] == 1
        assert response_json['items'][0]['price'] == '55.00'
        assert response_json['total_price'] == '55.00'

        cart_in_db = Cart.objects.get(user=user)
        assert cart_in_db.items.count() == 1
        assert cart_in_db.items.first().menu_item.id == menu_item.id

    def test_add_existing_item_updates_quantity(self, authenticated_client, create_cart_with_items):
        user = authenticated_client[1]
        
        ing_bread = IngredientFactory(name="Bread for Sandwich", _stored_qty=10)  # Unique name
        menu_item_initial = MenuItemFactory(name="Sandwich", base_price=70.00, ingredients=[ing_bread])
        dough_type_initial = DoughTypeFactory(name="white dough", extra_price=0.00, is_available=True)
        cart = CartFactory(user=user)  # Create cart via factory
        CartItemFactory(cart=cart, menu_item=menu_item_initial, dough_type=dough_type_initial, quantity=1)
        
        initial_item_count = cart.items.count()

        data = {
            "menu_item_id": menu_item_initial.id,
            "dough_type_id": dough_type_initial.id,
            "quantity": 2,  # Add 2 more to existing 1
        }

        response = authenticated_client[0].post('/api/eshop/cart/items/', data, format='json')

        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json['items']) == initial_item_count
        assert response_json['items'][0]['quantity'] == 3
        assert response_json['total_price'] == '210.00'

        cart_in_db = Cart.objects.get(user=user)
        assert cart_in_db.items.count() == initial_item_count
        assert cart_in_db.items.first().quantity == 3

    def test_add_item_invalid_menu_item_id(self, authenticated_client, create_dough_type):
        dough_type = DoughTypeFactory(name="white", extra_price=0.00, is_available=True)
        data = {
            "menu_item_id": 9999,
            "dough_type_id": dough_type.id,
            "quantity": 1
        }
        response = authenticated_client[0].post('/api/eshop/cart/items/', data, format='json')
        assert response.status_code == 400
        assert 'detail' in response.json()
        assert 'Menu item or dough type not found.' in response.json()['detail']
