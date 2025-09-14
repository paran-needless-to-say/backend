from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_transaction_trace(request):
    return Response({"message": "Transaction trace endpoint working"})