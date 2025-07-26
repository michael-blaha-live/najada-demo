import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem
from api.eshop.models.order import Order
from api.eshop.models.order_item import OrderItem
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.dough_type import DoughType
from api.eshop.models.ingredient import Ingredient
from api.eshop.models.payment_type import PaymentType
from api.eshop.services.cart import CartService
from decimal import Decimal


@pytest.mark.django_db
class TestOrderPost:

    def test_place_valid_order_from_populated_cart(
        self, authenticated_client,
        ingredient_factory, dough_type_factory, menu_item_factory, payment_type_factory,
        cart_item_factory
    ):
        client, user = authenticated_client
        
        # Arrange: Create ingredients with unique names using factory
        ing_bread = ingredient_factory(name="Bread_Test1", _stored_qty=100)
        ing_chicken = ingredient_factory(name="Chicken_Test1", _stored_qty=100)
        ing_salad = ingredient_factory(name="Salad_Test1", _stored_qty=100)
        ing_cheese = ingredient_factory(name="Cheese_Test1", _stored_qty=100)
        ing_milk = ingredient_factory(name="Milk_Test1", _stored_qty=100)

        dough_sv_l = dough_type_factory(name="světlá_Test1", extra_price=Decimal('0.00'))
        dough_cel = dough_type_factory(name="celozrnná_Test1", extra_price=Decimal('10.00'))

        mi_chicken_sandwich = menu_item_factory(name="Chicken Sandwich_Test1", base_price=Decimal('100.00'), ingredients=[ing_bread, ing_chicken, ing_salad])
        mi_cheese_sandwich = menu_item_factory(name="Cheese Sandwich_Test1", base_price=Decimal('80.00'), ingredients=[ing_bread, ing_cheese, ing_milk])

        cart, _ = Cart.objects.get_or_create(user=user)
        # Use cart_item_factory fixture directly
        cart_item_factory(cart=cart, menu_item=mi_chicken_sandwich, dough_type=dough_sv_l, quantity=1)
        cart_item_factory(cart=cart, menu_item=mi_cheese_sandwich, dough_type=dough_cel, quantity=2)

        assert cart.items.count() == 2
        assert Ingredient.objects.get(id=ing_bread.id)._stored_qty == 100
        
        expected_cart_total = sum(item.price * item.quantity for item in cart.items.all())
        payment_type = payment_type_factory(name="cash_Test1")

        data = {
            "cart_id": cart.id,
            "payment_type_id": payment_type.id,
        }
        expected_cart_total = sum(item.price * item.quantity for item in cart.items.all())
        response = client.post('/api/eshop/orders/create/', data, format='json')

        assert response.status_code == 201
        response_json = response.json()
        assert 'id' in response_json
        assert response_json['status'] == 'Created'

        order_in_db = Order.objects.get(id=response_json['id'])
        assert order_in_db.user == user
        assert order_in_db.payment_type == payment_type
        assert order_in_db.status == 'Created'
        
        assert order_in_db.total_price == expected_cart_total

        assert order_in_db.items.count() == 2
        
        order_item1 = order_in_db.items.get(menu_item_snapshot=mi_chicken_sandwich)
        assert order_item1.quantity == 1
        assert order_item1.unit_price_at_order == (Decimal('100.00') + Decimal('0.00'))

        order_item2 = order_in_db.items.get(menu_item_snapshot=mi_cheese_sandwich)
        assert order_item2.quantity == 2
        assert order_item2.unit_price_at_order == (Decimal('80.00') + Decimal('10.00'))

        assert Ingredient.objects.get(id=ing_bread.id)._stored_qty == 100 - 3
        assert Ingredient.objects.get(id=ing_chicken.id)._stored_qty == 100 - 1
        assert Ingredient.objects.get(id=ing_salad.id)._stored_qty == 100 - 1
        assert Ingredient.objects.get(id=ing_cheese.id)._stored_qty == 100 - 2
        assert Ingredient.objects.get(id=ing_milk.id)._stored_qty == 100 - 2

        cart_after_order = Cart.objects.get(user=user)
        assert cart_after_order.items.count() == 0

    def test_place_order_empty_cart(
        self, authenticated_client, payment_type_factory
    ):
        client, user = authenticated_client
        
        cart, _ = Cart.objects.get_or_create(user=user)
        cart.items.all().delete()

        payment_type = payment_type_factory(name="cash_EmptyCart")
        data = {
            "cart_id": cart.id,
            "payment_type_id": payment_type.id,
        }

        response = client.post('/api/eshop/orders/create/', data, format='json')

        assert response.status_code == 400
        assert response.json()['detail'] == 'Cart is empty.'
        assert Order.objects.count() == 0

    def test_place_order_invalid_payment_type(
        self, authenticated_client, ingredient_factory, dough_type_factory, menu_item_factory,
        cart_item_factory
    ):
        client, user = authenticated_client
        
        ing_test = ingredient_factory(name="TestIngredientInvalidPay", _stored_qty=10)
        dough_test = dough_type_factory(name="TestDoughInvalidPay", extra_price=Decimal('0.00'))
        mi_test = menu_item_factory(name="TestSandwichInvalidPay", base_price=Decimal('50.00'), ingredients=[ing_test])

        cart, _ = Cart.objects.get_or_create(user=user)
        # Use cart_item_factory fixture directly
        cart_item_factory(cart=cart, menu_item=mi_test, dough_type=dough_test, quantity=1)

        data = {
            "cart_id": cart.id,
            "payment_type_id": 9999,
        }

        response = client.post('/api/eshop/orders/create/', data, format='json')

        assert response.status_code == 400
        assert 'detail' in response.json()
        assert Order.objects.count() == 0
        assert cart.items.count() == 1

    def test_place_order_unavailable_item_stock_shortage(
        self, authenticated_client, ingredient_factory, dough_type_factory, menu_item_factory, payment_type_factory,
        cart_item_factory
    ):
        client, user = authenticated_client
        
        ing_race_condition = ingredient_factory(name="RaceCondIngTest", _stored_qty=1)
        
        dough_sv_la = dough_type_factory(name="RaceCondDoughType", extra_price=Decimal('0.00'))
        mi_race = menu_item_factory(name="RaceCondItemTest", base_price=Decimal('100.00'), ingredients=[ing_race_condition])

        cart, _ = Cart.objects.get_or_create(user=user)
        # Use CartItemFactory directly if available via fixture
        cart_item_factory(cart=cart, menu_item=mi_race, dough_type=dough_sv_la, quantity=1)

        payment_type = payment_type_factory(name="RaceCondPaymentType")
        data = {
            "cart_id": cart.id,
            "payment_type_id": payment_type.id,
        }
        
        ing_race_condition._stored_qty = 0
        ing_race_condition.save()
        
        ing_id_before_order = ing_race_condition.id

        response = client.post('/api/eshop/orders/create/', data, format='json')

        assert response.status_code == 400
        assert 'detail' in response.json()
        assert "Menu item 'RaceCondItemTest' is not available (base item unavailable)." == response.json()['detail']

        assert Order.objects.count() == 0

        assert Ingredient.objects.get(id=ing_id_before_order)._stored_qty == 0

        cart_after_order = Cart.objects.get(user=user)
        assert cart_after_order.items.count() == 1

    def test_place_order_unauthorized_access(self, api_client):
        response = api_client.post('/api/eshop/orders/create/', {}, format='json')
        assert response.status_code == 403
