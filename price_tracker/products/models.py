from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    url = models.URLField(
        'Ссылка'
    )
    name = models.CharField(
        'Название',
        max_length=255,
        blank=True,
        default='',
    )
    current_price = models.DecimalField(
        'Текущая стоимость',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    target_price = models.DecimalField(
        'Целевая стоимость',
        max_digits=10,
        decimal_places=2,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    def __str__(self):
        return self.name
    
    @property
    def status(self):
        if self.current_price is None:
            return 'Цена не определена'
        if self.current_price <= self.target_price:
            return 'Цена достигла целевого уровня'
        return 'Цена выше целевого уровня'

class PriceHistory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='price_history',
        verbose_name='Продукт',
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
    )
    timestamp = models.DateTimeField(
        'Дата и время',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.price} в {self.timestamp}'
