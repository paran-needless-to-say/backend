from rest_framework import serializers


class NextHopsRequestSerializer(serializers.Serializer):
    address = serializers.CharField(help_text="분석할 주소", required=True)
    network = serializers.CharField(help_text="네트워크 (예: eth-mainnet)", default="eth-mainnet")
    max_hops = serializers.IntegerField(help_text="최대 탐색 hop 수", default=2)