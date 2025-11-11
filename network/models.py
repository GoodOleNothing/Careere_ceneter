from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class NetworkNode(models.Model):
    """
    Узел сети (завод/розничная сеть/ИП)
    """
    name = models.CharField(max_length=200, verbose_name="Узел")
    email = models.EmailField()
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house_number = models.CharField(max_length=50, verbose_name="Номер дома")

    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clients",
        verbose_name="Поставщик"
    )

    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Задолженность"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    level = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name="Уровень")

    class Meta:
        verbose_name = "Узел сети"
        verbose_name_plural = "Узлы сети"

    # Уровень узла
    def clean(self):
        if self.supplier:
            if self.supplier_id == self.pk:
                calculated_level = 0
            else:
                calculated_level = (self.supplier.level or 0) + 1
        else:
            calculated_level = 0

        if calculated_level > 2:
            raise ValidationError(
                {"supplier": "Узел не может быть выше уровня 2"}
            )

    def save(self, *args, **kwargs):
        self.clean()

        if self.supplier:
            self.level = (self.supplier.level or 0) + 1
        else:
            self.level = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (уровень {self.level})"


class Product(models.Model):
    node = models.ForeignKey(NetworkNode, related_name="products", on_delete=models.CASCADE, verbose_name="Узел")
    name = models.CharField(max_length=200, verbose_name="Название")
    model = models.CharField(max_length=200, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата запуска")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} {self.model}"
