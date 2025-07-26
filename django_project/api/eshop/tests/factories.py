import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from api.eshop.models.dough_type import DoughType
from api.eshop.models.ingredient import Ingredient
from api.eshop.models.menu_item import MenuItem
from api.eshop.models.payment_type import PaymentType
from api.eshop.models.cart import Cart
from api.eshop.models.cart_item import CartItem


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True
    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_active = True


class DoughTypeFactory(DjangoModelFactory):
    class Meta:
        model = DoughType
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: f'DoughType {n}')
    extra_price = factory.Faker('pyint', min_value=0, max_value=1000)  # Corrected
    is_available = True


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = Ingredient
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: f'Ingredient {n}')
    _stored_qty = 100


class PaymentTypeFactory(DjangoModelFactory):
    class Meta:
        model = PaymentType
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: f'Payment {n}')


class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = MenuItem
        skip_postgeneration_save = True
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: f'MenuItem {n}')
    base_price = factory.Faker('pyint', min_value=0, max_value=1000)

    @factory.post_generation
    def ingredients(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for ingredient in extracted:
                self.ingredients.add(ingredient)


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart
    user = factory.SubFactory(UserFactory)


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem
    cart = factory.SubFactory(CartFactory)
    menu_item = factory.SubFactory(MenuItemFactory)
    dough_type = factory.SubFactory(DoughTypeFactory)
    quantity = 1
    note = ""
