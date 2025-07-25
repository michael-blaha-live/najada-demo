from django.urls import include, path
from api.eshop.views.health import health_view

urlpatterns = [
    path('heartbeat', health_view)
]
