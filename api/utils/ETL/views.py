from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.etl.services import get_transaction_trace


@api_view(['GET'])
def get_transaction_data(request):
    start_block = request.query_params.get("start_block")
    end_block = request.query_params.get("end_block")

    result = get_transaction_trace(start_block, end_block)
    return Response(result)