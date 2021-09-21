from rest_framework import serializers
from api.models import TestModel, OtherTestModel


class DumbSerializer(serializers.Serializer):
    hello = serializers.CharField()


class OtherTestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherTestModel
        fields = ["id"]


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = (
            "char_field",
            "email_field",
            # "created_at",
            # "file_field",
            "foreign_key",
            # "id",
            # "image_field",
            # "json_field",
            # "many_to_many_field",
            # "one_to_one_field",
            # "text_field",
            # "updated_at",
            # # "many",
            # "fks",
            # "ones",
        )

        extra_kwargs = {"char_field": {"default": "hello"}}


OtherTestSerializer = TestSerializer
