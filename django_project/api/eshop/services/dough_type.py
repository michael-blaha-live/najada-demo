from django.db.models import QuerySet

from api.eshop.core.singleton import Singleton
from api.eshop.models.dough_type import DoughType


class DoughTypeService(metaclass=Singleton):
    @staticmethod
    def get_all_dough_types() -> QuerySet[DoughType]:
        """
        Retrieves all DoughType instances from the database.
        """
        return DoughType.objects.all()

    @staticmethod
    def get_dough_type_by_id(dough_type_id: int) -> DoughType | None:
        """
        Retrieves a specific DoughType instance by its ID.
        """
        try:
            return DoughType.objects.get(id=dough_type_id)
        except DoughType.DoesNotExist:
            return None
