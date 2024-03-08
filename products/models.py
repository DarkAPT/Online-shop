from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='products_images')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    categoryid = models.ForeignKey(to=Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Properties(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    valueType = models.CharField(max_length=150)

    class Meta:
        db_table = 'properties'
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'


class PropertyValues(models.Model):
    propertyid = models.ForeignKey(to=Properties, on_delete=models.CASCADE)
    value = models.CharField(max_length=150)

    class Meta:
        db_table = 'PropertyValues'
        verbose_name = 'Значения свойств'


class CharacteristicsSet(models.Model):
    productid = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    propertyid = models.ForeignKey(to=Properties, on_delete=models.CASCADE)
    propertyvalueid = models.ForeignKey(to=PropertyValues, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CharacteristicsSet'
        verbose_name = 'Набор свойств'
