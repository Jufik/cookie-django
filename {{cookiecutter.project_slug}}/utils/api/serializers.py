from rest_framework.serializers import ModelSerializer as BaseModelSerializer
import copy

from collections import OrderedDict

from rest_framework.settings import api_settings
from rest_framework.utils import model_meta


class ModelSerializer(BaseModelSerializer):
    pass

