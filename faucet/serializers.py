from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    account = serializers.RegexField('^[a-z0-9.-]{3,32}$')


class SignUpWithKeysSerialzer(BaseSerializer):
    active_key = serializers.CharField()
    memo_key = serializers.CharField()
    owner_key = serializers.CharField()


class SignUpWithPasswordSerialzer(BaseSerializer):
    password = serializers.RegexField('^[\S]{12,32}$')
