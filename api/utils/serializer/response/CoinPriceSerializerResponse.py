from rest_framework import serializers


class CoinPriceSerializerResponse(serializers.Serializer):
    coin = serializers.CharField()
    currency = serializers.CharField()
    price = serializers.FloatField()
