from django.urls import path, include
from api.eshop import urls as eshop_urls


urlpatterns = [
    path(r'eshop/', include(eshop_urls))
]
