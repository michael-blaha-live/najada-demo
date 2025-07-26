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
class TestCartDeleteItem:
    def test_delete_item_from_cart(self, authenticated_client, create_cart_with_items):
        user = authenticated_client[1]
        items_data = [
            {"menu_item_name": "Test1", "base_price": 50, "ingredients": ["A"], "dough_type_name": "white", "extra_price": 0, "quantity": 2}
        ]
        cart = create_cart_with_items(user, items_data)
        cart_item_id = cart.items.first().id

        response = authenticated_client[0].delete(f'/api/eshop/cart/items/{cart_item_id}/')

        assert response.status_code == 204
        assert not CartItem.objects.filter(id=cart_item_id).exists()
        
        cart_in_db = Cart.objects.get(user=user)
        assert cart_in_db.items.count() == 0
        assert cart_in_db.total_price == 0

    def test_delete_item_not_found(self, authenticated_client):
        response = authenticated_client[0].delete('/api/eshop/cart/items/9999/')
        assert response.status_code == 404
