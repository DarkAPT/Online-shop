from django.db import models
from products.models import Products

from users.models import User


class OrderItemQueryset(models.QuerySet):
    def total_price(self):
        temp =  sum(cart.product_price_for_carts() for cart in self)
        return '{:,}'.format(temp).replace(',', ' ')

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,blank=True, null=True, verbose_name="Пользователь", default=None)
    create_data = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default="В обработке", verbose_name="Статус заказа")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f'Заказ № {self.pk} | Покупатель {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, default=None, verbose_name="Продукт")
    name = models.CharField(verbose_name="Название")
    price = models.PositiveIntegerField(verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")

    objects = OrderItemQueryset.as_manager()

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def products_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f'Товар {self.product} | Заказ №{self.order.pk}'
