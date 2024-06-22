from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('catalog-gpu/', views.catalog_gpu, name='catalog-gpu'),
    path('catalog-cpu/', views.catalog_cpu, name='catalog-cpu'),
    path('catalog-motherboard/', views.catalog_motherboard, name='catalog-motherboard'),
    path('catalog-ram/', views.catalog_ram, name='catalog-ram'),
    path('catalog-ssd/', views.catalog_ssd, name='catalog-ssd'),
]
