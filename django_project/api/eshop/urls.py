from django.urls import include, path
from api.eshop.views.heartbeat import HeartbeatAPIView
from api.eshop.views.dough_type_list import DoughTypeListAPIView
from api.eshop.views.dough_type_detail import DoughTypeDetailAPIView
from api.eshop.views.payment_type_list import PaymentTypeListAPIView
from api.eshop.views.ingredient_list import IngredientListAPIView
from api.eshop.views.menu_item_list import MenuItemListAPIView
from api.eshop.views.cart_detail import CartDetailAPIView
from api.eshop.views.cart_item_add import CartItemAddAPIView
from api.eshop.views.cart_item_detail import CartItemDetailAPIView
from api.eshop.views.order_create import OrderCreateAPIView
from api.eshop.views.order_list import OrderListAPIView
from api.eshop.views.order_detail import OrderDetailAPIView

urlpatterns = [
    path('heartbeat/', HeartbeatAPIView.as_view(), name='heartbeat'),
    path('dough-types/', DoughTypeListAPIView.as_view(), name='dough-type-list'),
    path('dough-types/<int:pk>/', DoughTypeDetailAPIView.as_view(), name='dough-type-detail'),
    path('payment-types/', PaymentTypeListAPIView.as_view(), name='payment-type-list'),
    path('ingredients/', IngredientListAPIView.as_view(), name='ingredient-list'),
    path('menu-items/', MenuItemListAPIView.as_view(), name='menu-item-list'),
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/items/', CartItemAddAPIView.as_view(), name='cart-item-add'),
    path('cart/items/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
