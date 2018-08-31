import factory

from emailauth.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    is_staff = factory.Faker('pybool')
    is_active = factory.Faker('pybool')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)

        # this might not properly works
        # noqa
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)