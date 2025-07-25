from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_dough_type_view(request):
    """Returns dough type list."""
    return Response({'healthy': True})
