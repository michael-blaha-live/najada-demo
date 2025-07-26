from django.db.models import QuerySet

from api.eshop.core.singleton import Singleton
from api.eshop.models.payment_type import PaymentType


class PaymentTypeService(metaclass=Singleton):
    @staticmethod
    def get_all_payment_types() -> QuerySet[PaymentType]:
        """
        Retrieves all PaymentType instances from the database.
        """
        return PaymentType.objects.all()
