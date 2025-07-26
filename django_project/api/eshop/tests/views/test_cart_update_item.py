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


@pytest.mark.django_db
class TestCartUpdateItem:
    def test_update_item_quantity(self, authenticated_client, create_cart_with_items, ingredient_factory):
        user = authenticated_client[1]
        ingredient_factory(name="A", _stored_qty=100)
        items_data = [
            {"menu_item_name": "Test1", "base_price": 50, "ingredients": ["A"], "dough_type_name": "white", "extra_price": 0, "quantity": 2}
        ]
        cart = create_cart_with_items(user, items_data)
        cart_item_id = cart.items.first().id

        data = {"quantity": 5}
        response = authenticated_client[0].patch(f'/api/eshop/cart/items/{cart_item_id}/', data, format='json')
        print(response.json())

        assert response.status_code == 200
        response_json = response.json()
        assert response_json['items'][0]['quantity'] == 5
        assert response_json['total_price'] == '250.00'

        cart_item_in_db = CartItem.objects.get(id=cart_item_id)
        assert cart_item_in_db.quantity == 5

    def test_update_item_set_quantity_to_zero_removes_item(self, authenticated_client, create_cart_with_items):
        user = authenticated_client[1]
        items_data = [
            {"menu_item_name": "Test1", "base_price": 50, "ingredients": ["A"], "dough_type_name": "white", "extra_price": 0, "quantity": 2}
        ]
        cart = create_cart_with_items(user, items_data)
        cart_item_id = cart.items.first().id

        data = {"quantity": 0}
        response = authenticated_client[0].patch(f'/api/eshop/cart/items/{cart_item_id}/', data, format='json')

        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json['items']) == 0
        assert response_json['total_price'] == '0.00'

        assert not CartItem.objects.filter(id=cart_item_id).exists()

    def test_update_item_not_found(self, authenticated_client):
        response = authenticated_client[0].patch('/api/eshop/cart/items/9999/', {"quantity": 1}, format='json')
        assert response.status_code == 404
