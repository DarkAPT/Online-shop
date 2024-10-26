from django.db import models
from products.models import Products
from users.models import User


class CartQuerySet(models.QuerySet):

    def total_price(self):
        temp =  sum(cart.product_price_for_carts() for cart in self)
        return '{:,}'.format(temp).replace(',', ' ')

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    session_key = models.CharField(max_length=32,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name="Корзина"
        verbose_name_plural="Корзина"

    objects = CartQuerySet().as_manager()

    def product_price(self):
        total_price =  self.product.sell_price_for_carts() * self.quantity
        return '{:,}'.format(total_price).replace(',', ' ')

    def product_price_for_carts(self):
        return self.product.sell_price_for_carts() * self.quantity

    def __str__(self) -> str:
        return f'Корзина {self.user.username} - Товар {self.product.name} Количество {self.quantity}'
    