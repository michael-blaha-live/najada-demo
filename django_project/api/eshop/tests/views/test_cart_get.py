import pytest
from rest_framework.test import APIClient
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.dough_type import DoughType
from api.eshop.serializers.cart import CartSerializer


@pytest.mark.django_db
class TestGetCart:

    def test_get_empty_cart(self, authenticated_client):
        """
        GIVEN an authenticated user with an empty cart
        WHEN a GET request is made to /api/eshop/cart/
        THEN the API should return 200 OK with an empty cart structure.
        """
        client, user = authenticated_client
        response = client.get('/api/eshop/cart/')  # Use the client object

        assert response.status_code == 200
        # Expected structure for an empty cart
        assert response.json() == {
            'id': Cart.objects.get(user=user).id,  # Cart ID will exist even if empty
            'total_price': '0.00',
            'vat': '0.00',
            'wo_vat_price': '0.00',
            'items': []
        }

    def test_get_cart_with_items(self, authenticated_client, create_cart_with_items):
        """
        GIVEN an authenticated user with a cart containing items
        WHEN a GET request is made to /api/eshop/cart/
        THEN the API should return 200 OK with the populated cart data and correct totals.
        """
        client, user = authenticated_client
        # Arrange: Define items to put in the cart
        items_data = [
            {
                "menu_item_name": "Cézar", "base_price": 100.00, "ingredients": ["Kuřecí maso"],
                "dough_type_name": "světlá", "extra_price": 0.00, "quantity": 1, "note": "No pickles"
            },
            {
                "menu_item_name": "Šunková", "base_price": 150.00, "ingredients": ["Šunka"],
                "dough_type_name": "celozrnná", "extra_price": 10.00, "quantity": 2
            },
        ]
        cart = create_cart_with_items(user, items_data)
        
        # Expected calculations:
        # Item 1: Cézar (100.00) + světlá (0.00) * 1 = 100.00
        # Item 2: Šunková (150.00) + celozrnná (10.00) * 2 = 160.00 * 2 = 320.00
        # Total: 100.00 + 320.00 = 420.00 (assuming no VAT for now, or 0% VAT)
        # For simplicity, let's assume VAT is 0 for testing price
        expected_total_price = '420.00'
        expected_vat = '0.00'
        expected_wo_vat_price = '420.00'

        response = client.get('/api/eshop/cart/')

        assert response.status_code == 200
        response_json = response.json()

        assert response_json['id'] == cart.id
        assert response_json['total_price'] == expected_total_price
        assert response_json['vat'] == expected_vat
        assert response_json['wo_vat_price'] == expected_wo_vat_price
        assert len(response_json['items']) == 2

        # Sort items for comparison consistency
        response_items_sorted = sorted(response_json['items'], key=lambda x: x['menu_item_id'])
        
        # Verify structure of first item
        assert response_items_sorted[0]['menu_item_id'] == cart.items.all()[0].menu_item.id
        assert response_items_sorted[0]['dough_type_id'] == cart.items.all()[0].dough_type.id
        assert response_items_sorted[0]['quantity'] == 1
        assert response_items_sorted[0]['price'] == '100.00'  # 100.00 + 0.00
        assert response_items_sorted[0]['note'] == 'No pickles'
        
        # Verify structure of second item
        assert response_items_sorted[1]['menu_item_id'] == cart.items.all()[1].menu_item.id
        assert response_items_sorted[1]['dough_type_id'] == cart.items.all()[1].dough_type.id
        assert response_items_sorted[1]['quantity'] == 2
        assert response_items_sorted[1]['price'] == '160.00'  # 150.00 + 10.00
        assert response_items_sorted[1]['note'] == ''
