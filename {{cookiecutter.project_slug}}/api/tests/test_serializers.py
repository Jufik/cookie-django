from api.serializers import ModelSerializer
from api.models import TestModel


def test_model_serializer_registers_serializer_to_models(
    db, 
):
    assert getattr(TestModel, "serializers", None) is None

