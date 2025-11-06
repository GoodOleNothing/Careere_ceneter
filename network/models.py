from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class NetworkNode(models.Model):
    """
    Узел сети (завод / розничная сеть / ИП)
    """
    name = models.CharField(max_length=200)

    # Контакты
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=50)

    # Поставщик (ссылка на другой узел сети, может быть null => уровень 0 (завод))
    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clients"
    )

    # Задолженность перед поставщиком
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    level = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "Узел сети"
        verbose_name_plural = "Узлы сети"

    def save(self, *args, **kwargs):
        # вычисляем уровень: если supplier указан -> supplier.level + 1, иначе 0
        if self.supplier:
            # на случай циклической ссылки — защищаем: если supplier == self -> treat as 0
            if self.supplier_id == self.pk:
                self.level = 0
            else:
                # Если supplier.level слишком велик (например 2), запретим уровни > 2
                self.level = (self.supplier.level or 0) + 1
        else:
            self.level = 0

        # ограничение трехуровневой структуры: 0,1,2
        if self.level > 2:
            raise ValueError("Уровень узла не может быть больше 2 (макс. три уровня: завод, розница, ИП).")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (уровень {self.level})"


class Product(models.Model):
    node = models.ForeignKey(NetworkNode, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    release_date = models.DateField()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} {self.model}"
