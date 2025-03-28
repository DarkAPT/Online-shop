# Generated by Django 4.2.7 on 2024-07-11 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('valueType', models.CharField(blank=True, max_length=150, null=True)),
                ('categoryid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categories')),
            ],
            options={
                'verbose_name': 'Свойство',
                'verbose_name_plural': 'Свойства',
                'db_table': 'properties',
            },
        ),
        migrations.CreateModel(
            name='PropertyValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=150)),
                ('propertyid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.properties')),
            ],
            options={
                'verbose_name': 'Значения свойств',
                'db_table': 'PropertyValues',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='URL')),
                ('image', models.ImageField(upload_to='products_images')),
                ('description', models.TextField(blank=True, null=True)),
                ('brand_image', models.ImageField(upload_to='brand_icons')),
                ('price', models.PositiveIntegerField(default=0)),
                ('discount', models.PositiveIntegerField(default=0)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('categoryid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categories')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='CharacteristicsSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('propertyid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.properties')),
                ('propertyvalueid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.propertyvalues')),
            ],
            options={
                'verbose_name': 'Набор свойств',
                'db_table': 'CharacteristicsSet',
            },
        ),
    ]
