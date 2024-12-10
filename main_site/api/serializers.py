from rest_framework import serializers


class GetSubGroupsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class GetSubGroupsSerializerList(serializers.Serializer):
    subgroups = serializers.ListField(child=GetSubGroupsSerializer())


class GetServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class GetServiceSerializerList(serializers.Serializer):
    services = serializers.ListField(child=GetServiceSerializer())
