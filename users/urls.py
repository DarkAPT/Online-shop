from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('favourites/', views.FavouritesView.as_view(), name='favourites')
]
