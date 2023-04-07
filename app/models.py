from django.conf import settings
from django.db import models
from django.forms import forms


class Order(models.Model):
    id = models.IntegerField(verbose_name='№', primary_key=True)
    order_number = models.IntegerField(verbose_name='номер заказа')
    prise_usd = models.IntegerField(verbose_name='цена в долларах')
    delivery_time = models.DateField(verbose_name='срок поставки')
    prise_rub = models.IntegerField(verbose_name='цена в рублях')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    # def __str__(self):
    #     return self.order_number
