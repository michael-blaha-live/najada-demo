from api.eshop.core.singleton import Singleton
from api.eshop.models.menu_item import MenuItem
from django.db.models import QuerySet


class MenuItemService(metaclass=Singleton):
    @staticmethod
    def get_all_menu_items() -> QuerySet[MenuItem]:
        return MenuItem.objects.all()

    @staticmethod
    def get_menu_item_by_id(menu_item_id: int) -> MenuItem | None:
        try:
            return MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return None
