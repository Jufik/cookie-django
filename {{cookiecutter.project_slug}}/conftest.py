import pytest, logging, importlib
from django.apps import apps
from pytest_factoryboy import register

from main.urls.api import router
from utils.tests.conftest import DRFClient

logger = logging.getLogger("Conftest")


def generate_client(name):
    @pytest.fixture(name=f"{name}_api_client")
    def wrapped(db):
        return DRFClient(ressource=name)

    return f"{name}_api_client", wrapped


for endpoint, view, name in router.registry:
    n, f = generate_client(name)
    logger.info(f"Created fixture: {n}")
    globals()[n] = f

for model in apps.get_models():
    try:
        module = importlib.import_module(f"model_factories.{model._meta.app_label}")
        factory = getattr(module, f"{model.__name__}Factory")
        register(factory)
        logger.info(f"Created fixture for: {model.__name__}")
    except ImportError:
        logger.warning(
            f"Could not create fixture for {model.__name__}, model_factories.{model._meta.app_label}.{model.__name__}Factory not found"
        )
