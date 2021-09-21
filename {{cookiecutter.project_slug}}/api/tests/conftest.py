import pytest
from pytest_factoryboy import register
import factory

import pytest
from utils.api import serializers
from api.models import TestModel, TestThrough, OtherTestModel
from model_factories.api import (
    TestModelFactory,
    TestThroughFactory,
    OtherTestModelFactory,
)

register(TestModelFactory)
register(TestThroughFactory)
register(
    OtherTestModelFactory,
    foreign_key=None,
    one_to_one_field=None,
    many_to_many_field_with_through=None,
)


@pytest.fixture
def model_serializer_factory(db):
    def factory(field, attrs={}, meta_extra_kwargs={}):
        class Meta:
            model = TestModel
            fields = [field, *attrs.keys()]
            extra_kwargs = meta_extra_kwargs

        return type(
            f"TestModelSerializerFor{field}",
            (serializers.ModelSerializer,),
            {"Meta": Meta, **attrs},
        )()

    return factory

