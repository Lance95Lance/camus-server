from rest_framework import serializers


class IdNumberSerializer(serializers.Serializer):
    area_id = serializers.StringRelatedField()
    area_name = serializers.StringRelatedField()
    birthday = serializers.StringRelatedField()
    age = serializers.IntegerField()
    sex = serializers.StringRelatedField()
    check_digit = serializers.StringRelatedField()
    facticity = serializers.StringRelatedField()
