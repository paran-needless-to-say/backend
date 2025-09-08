from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import get_next_hops


@api_view(['POST'])
def next_hops(request):
    address = request.data.get("address")
    network = request.data.get("network")
    max_hops = request.data.get("max_hops")

    result = get_next_hops(address, network, max_hops)
    return Response(result)
