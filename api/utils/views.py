from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from api.utils.serializer.response.CoinPriceSerializerResponse import CoinPriceSerializerResponse
from api.utils.services import get_token_price


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="token",
            description="코인 심볼 (예: BTC, ETH, USDT)",
            required=True,
            type=str,
            location=OpenApiParameter.QUERY,
        )
    ],
    responses=CoinPriceSerializerResponse
)
@api_view(['GET'])
def get_coin_price(request):
    token = request.query_params.get("token")
    if not token:
        return Response({"error": "coin parameter is required"}, status=400)

    result = get_token_price(token)

    if not result:
        return Response({"error": f"Failed to fetch price for '{token}'"}, status=500)

    return Response(result)
