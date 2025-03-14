from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from carts.models import Cart
from orders.models import Order, OrderItem

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
        return HttpResponseRedirect(self.success_url)

class UserProfileView(LoginRequiredMixin ,UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['orders'] = (
        Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by('-id')
    )
        return context

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


class CartView(TemplateView):
    """Страница корзины"""
    template_name = "users/cart.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Корзина"
        return context

class FavouritesView(TemplateView):
    """Страница избранных товаров"""
    template_name = "users/favourites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Избранное'
        return context
    