from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.category_prediction, name='category_prediction'),
    path('<slug:category_slug>/', views.catalog, name='catalog'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]
