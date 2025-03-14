from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('review/', views.ReviewView.as_view(), name='review'),
    path('update_review/', views.UpdateReviewView.as_view(), name='update_review'),
    path('', views.CategoryPredictionView.as_view(), name='category_prediction'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]
