from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='products_images')
    description = models.TextField(blank=True, null=True)
    brand_image = models.ImageField(upload_to='brand_icons')
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    categoryid = models.ForeignKey(to=Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id", )

    def __str__(self) -> str:
        return f'{self.name}, Кол-во - {self.quantity}'

    def display_id(self):
        return f'{self.id:05}'

    def price_without_disc(self):
        return '{:,}'.format(self.price).replace(',', ' ')

    def sell_price(self):
        price = int(self.price - self.price * self.discount / 100)
        return '{:,}'.format(price).replace(',', ' ')

    @staticmethod
    def get_most_expensive_product():
        return Products.objects.order_by('-price').first()



class Properties(models.Model):
    name = models.CharField(max_length=150, unique=True)
    valueType = models.CharField(max_length=150, blank=True, null=True)
    categoryid = models.ForeignKey(to=Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'properties'
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'

    def __str__(self) -> str:
        return self.name


class PropertyValues(models.Model):
    propertyid = models.ForeignKey(to=Properties, on_delete=models.CASCADE)
    value = models.CharField(max_length=150)

    class Meta:
        db_table = 'PropertyValues'
        verbose_name = 'Значения свойств'

    def __str__(self) -> str:
        return f'{self.propertyid.name}: {self.value}'



class CharacteristicsSet(models.Model):
    productid = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    propertyid = models.ForeignKey(to=Properties, on_delete=models.CASCADE)
    propertyvalueid = models.ForeignKey(to=PropertyValues, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CharacteristicsSet'
        verbose_name = 'Набор свойств'

    def __str__(self) -> str:
        return f'{self.productid.name} - {self.propertyid.name}'
