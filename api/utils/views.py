from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.services import get_token_price


@api_view(['GET'])
def get_coin_price(request):
    token = request.query_params.get("token")
    if not token:
        return Response({"error": "coin parameter is required"}, status=400)

    result = get_token_price(token)

    if not result:
        return Response({"error": f"Failed to fetch price for '{token}'"}, status=500)

    return Response(result)
