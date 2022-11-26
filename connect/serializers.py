from rest_framework import serializers


class EligibilitySerializers(serializers.Serializer):
    phone_number = serializers.CharField()


class QueryTanadiDatabaseSerializers(serializers.Serializer):
    phone_number = serializers.CharField()