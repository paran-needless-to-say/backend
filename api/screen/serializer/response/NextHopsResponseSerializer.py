from rest_framework import serializers


class EvidenceSerializer(serializers.Serializer):
    type = serializers.CharField()
    hash = serializers.CharField()
    label = serializers.CharField()
    ts = serializers.CharField()
    url = serializers.CharField()


class NextHopsResponseSerializer(serializers.Serializer):
    summary = serializers.CharField()
    contrib = serializers.DictField()
    evidence = EvidenceSerializer(many=True)
    metrics = serializers.DictField()
    risk = serializers.CharField()
    rule_ids = serializers.ListField(child=serializers.CharField())
    policy_version = serializers.CharField()
    decision_id = serializers.CharField()