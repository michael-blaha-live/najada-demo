from django.urls import include, path
from api.eshop.views.health import health_view
from api.eshop.views.dough_type_list import DoughTypeListAPIView
from api.eshop.views.dough_type_detail import DoughTypeDetailAPIView

urlpatterns = [
    path('heartbeat', health_view),
    path('dough-types/', DoughTypeListAPIView.as_view(), name='dough-type-list'),
    path('dough-types/<int:pk>/', DoughTypeDetailAPIView.as_view(), name='dough-type-detail'),
]
