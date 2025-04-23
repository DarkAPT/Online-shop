from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.utils import activate_email
from .tokens import account_activation_token

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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = form.cleaned_data.get('email')
            domain = get_current_site(self.request).domain
            protocol = "https" if self.request.is_secure() else "http"
            activate_email.delay(user.id, email, domain, protocol)
            messages.success(self.request, "Проверьте почту, чтобы подтвердить аккаунт")
            return redirect("users:registration")
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
        return HttpResponseRedirect(self.success_url)

class ActivateView(View):
    template_name = "main/index.html"

    def get(self, request, uidb64, token):
        User = auth.get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except():
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(request, user)
            return redirect('main:index')
        else:
            messages.error(request, "Activation link is invalid!")
            return redirect('users:registration')


class UserProfileView(LoginRequiredMixin,CacheMixin ,UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        orders = (
        Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by('-id')
    )
        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60)
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
    