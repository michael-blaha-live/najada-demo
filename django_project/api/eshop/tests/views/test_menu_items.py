import pytest
from rest_framework.test import APIClient

from api.eshop.models.menu_item import MenuItem
from api.eshop.models.ingredient import Ingredient
from api.eshop.serializers.menu_item import MenuItemSerializer
from api.eshop.tests.factories import MenuItemFactory, IngredientFactory


@pytest.mark.django_db
class TestGetMenuItems:

    def test_get_menu_items_empty_list(self, api_client):
        response = api_client.get('/api/eshop/menu-items/')

        assert response.status_code == 200
        assert response.json() == []

    def test_get_menu_items_populated_list_all_available(self, api_client):
        # Arrange: Create ingredients (sufficient stock for is_available=True)
        ing_chicken = IngredientFactory(name="Kuřecí maso", _stored_qty=10)
        ing_lettuce = IngredientFactory(name="Římský salát", _stored_qty=10)
        ing_parmesan = IngredientFactory(name="Parmazán", _stored_qty=10)
        ing_ham = IngredientFactory(name="Šunka", _stored_qty=10)
        ing_cheese = IngredientFactory(name="Sýr", _stored_qty=10)
        ing_tomato = IngredientFactory(name="Rajče", _stored_qty=10)

        # Arrange: Create menu items, linking Ingredient instances
        menu_item1 = MenuItemFactory(
            name="Cézar", base_price=123.00,
            ingredients=[ing_chicken, ing_lettuce, ing_parmesan]
        )
        menu_item2 = MenuItemFactory(
            name="Šunková", base_price=234.00,
            ingredients=[ing_ham, ing_cheese, ing_tomato]  # Pass ingredient instances
        )

        response = api_client.get('/api/eshop/menu-items/')

        assert response.status_code == 200
        
        expected_data_list = MenuItemSerializer([menu_item1, menu_item2], many=True).data
        
        expected_data_list_sorted = sorted(expected_data_list, key=lambda item: item['name'])
        response_data_sorted = sorted(response.json(), key=lambda item: item['name'])
        
        assert response_data_sorted == expected_data_list_sorted
        assert all(item['is_available'] is True for item in response_data_sorted)

    def test_get_menu_items_some_unavailable_due_to_ingredient_stock(self, api_client):
        # Arrange: Create ingredients with varying stock
        ing_ham = IngredientFactory(name="Šunka", _stored_qty=1)  # Will be available
        ing_cheese_no_stock = IngredientFactory(name="Sýr (No Stock)", _stored_qty=0)  # Will be UNAVAILABLE
        ing_tomato = IngredientFactory(name="Rajče", _stored_qty=5)

        # Arrange: Create menu items
        menu_item_ham = MenuItemFactory(
            name="Šunková (Limited)", base_price=200.00,
            ingredients=[ing_ham, ing_tomato]  # Will be available
        )
        menu_item_cheese = MenuItemFactory(
            name="Sýrová (Unavailable)", base_price=150.00,
            ingredients=[ing_cheese_no_stock, ing_tomato]
        )

        response = api_client.get('/api/eshop/menu-items/')

        assert response.status_code == 200
        response_data = response.json()
        
        sunkova_limited = next((item for item in response_data if item['name'] == "Šunková (Limited)"), None)
        syrova_unavailable = next((item for item in response_data if item['name'] == "Sýrová (Unavailable)"), None)

        assert sunkova_limited is not None
        assert sunkova_limited['is_available'] is True

        assert syrova_unavailable is not None
        assert syrova_unavailable['is_available'] is False

        assert len(response_data) == 2
