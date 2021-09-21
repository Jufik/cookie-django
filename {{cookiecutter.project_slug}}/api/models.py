from utils import models
from api.options import BaseApi
from utils.models import Model

# Create your models here.


class CharChoices(models.TextChoices):
    HELLO = "HELLO", "hello"
    WORLD = "WORLD", "world"


class TestModel(Model):
    __test__ = False

    big_integer_field = models.BigIntegerField()
    binary_field = models.BinaryField()
    boolean_field = models.BooleanField()
    char_field = models.CharField(max_length=2555,)
    char_field_with_choices = models.CharField(
        max_length=255, choices=CharChoices.choices
    )
    date_field = models.DateField()
    date_time_field = models.DateTimeField()
    decimal_field = models.DecimalField(max_digits=5, decimal_places=2)
    duration_field = models.DurationField()
    email_field = models.EmailField(default="julien@mefa.tech")
    float_field = models.FloatField()
    generic_ip_address_field = models.GenericIPAddressField()
    integer_field = models.IntegerField()
    null_boolean_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    positive_small_integer_field = models.PositiveSmallIntegerField()
    slug_field = models.SlugField()
    small_integer_field = models.SmallIntegerField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField()
    uuid_field = models.UUIDField()
    foreign_key = models.ForeignKey(
        "api.OtherTestModel",
        on_delete=models.CASCADE,
        limit_choices_to={"char_field__icontains": "hello"},
        related_name="fks",
    )
    many_to_many_field = models.ManyToManyField(
        "api.OtherTestModel",
        related_name="many",
        limit_choices_to={"char_field__icontains": "world"},
    )
    one_to_one_field = models.OneToOneField(
        "api.OtherTestModel", on_delete=models.CASCADE, related_name="one"
    )
    file_field = models.FileField()
    image_field = models.ImageField()

    class Api(BaseApi):
        pass

    class Meta:
        verbose_name = "TestModel"
        verbose_name_plural = "Test Models"

    @property
    def dumb_property(self):
        return {"hello": "world"}


class TestThrough(Model):
    __test__ = False
    test = models.ForeignKey("api.TestModel", on_delete=models.CASCADE)
    other_test = models.ForeignKey("api.OtherTestModel", on_delete=models.CASCADE)

    class Api(BaseApi):
        pass

    class Meta:
        verbose_name = "TestThrough"
        verbose_name_plural = "TestThroughs"

    def __str__(self):
        return self.name


class OtherTestModel(Model):
    __test__ = False
    char_field = models.CharField(max_length=2555,)
    foreign_key = models.ForeignKey(
        "api.TestModel", on_delete=models.CASCADE, related_name="reverse_fks", null=True
    )
    one_to_one_field = models.OneToOneField(
        "api.TestModel", on_delete=models.CASCADE, related_name="reverse_one", null=True
    )
    many_to_many_field_with_through = models.ManyToManyField(
        "api.TestModel",
        related_name="reverse_many_with_through",
        through="api.TestThrough",
    )

    class Api(BaseApi):
        pass

    class Meta:
        verbose_name = "OtherTestModel"
        verbose_name_plural = "Other Test Models"

    def __str__(self):
        return self.name

