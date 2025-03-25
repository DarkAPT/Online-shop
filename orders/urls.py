from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path("payment_success/", views.PaymentSuccessView.as_view(), name="payment_success"),
    path("payment_failed/", views.PaymentFailedView.as_view(), name="payment_failed"),
]