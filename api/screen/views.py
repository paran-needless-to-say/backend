from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer.request.NextHopsRequestSerializer import NextHopsRequestSerializer
from .serializer.response.NextHopsResponseSerializer import NextHopsResponseSerializer
from .services import get_next_hops


@extend_schema(
    request=NextHopsRequestSerializer,
    responses=NextHopsResponseSerializer,
    summary="Next Hops 분석",
    description="주소와 네트워크를 입력받아 Bridge → Mixer 경로 등을 분석합니다."
)
@api_view(['POST'])
def next_hops(request):
    address = request.data.get("address")
    network = request.data.get("network")
    max_hops = request.data.get("max_hops")

    result = get_next_hops(address, network, max_hops)
    return Response(result)
