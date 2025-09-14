from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.etl.services import get_transaction_trace


@api_view(['GET'])
def get_transaction_data(request):
    result = get_transaction_trace()
    return Response(result)