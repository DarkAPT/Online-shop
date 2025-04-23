from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.db.models import F, ExpressionWrapper, FloatField
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from products.forms import ReviewForm
from products.utils import q_search
from products.models import Products,Properties,PropertyValues,Categories, Review
from products.utils import model,vectorizer

class ProductView(DetailView):
    """Страница товара"""
    model = Products
    template_name = "products/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.get_average_rating():
            average_rating, review_count = self.object.get_average_rating()
            context['average_rating'] = average_rating
            context['review_count'] = review_count
        context['title'] = self.object.name
        return context


class CatalogView(ListView):
    """Каталог товаров"""
    model = Products
    template_name = "products/catalog.html"
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self) :
        category_slug = self.kwargs.get("category_slug")
        query = self.request.GET.get('q', None)

        if query:
            products = q_search(query)
            products = products.filter(categoryid__slug=category_slug)
        else:
            products = super().get_queryset().filter(categoryid__slug=category_slug)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get("category_slug")

        context['title'] = Categories.objects.filter(slug = category_slug)[0].name
        context['properties'] = Properties.objects.filter(categoryid__slug=category_slug).values_list("name", flat=True)
        context["category_slug"] = category_slug
        return context


class ProductFiltersView(View):
    """Фильтр продуктов"""
    def get(self, request):
        filter_param = request.GET.getlist('filter[]')
        order_by = request.GET.get('order_by', 'new')
        category_slug = request.GET.get('category_slug')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        query = request.GET.get('q', None)
        page = request.GET.get('page')

        products = self.filtered_products(category_slug, query, filter_param, min_price, max_price)
        products = self.apply_sorting(products, order_by)

        if products:
            paginator = Paginator(products, 4)
            current_page = paginator.page(page)
            data = render_to_string('products/async/catalog.html', {'products': current_page, 'request': request})
        else:
            data = render_to_string('products/async/not_found_page.html')

        return JsonResponse({"data": data})

    def filtered_products(self, category_slug, query, filter_param, min_price, max_price):
        """Получения фильтрованных продуктов"""
        if query:
            products = q_search(query)
        else:
            products = Products.objects.filter(categoryid__slug=category_slug)

        if filter_param:
            products = self.apply_filters(products, filter_param)

        if min_price or max_price:
            products = self.filter_by_price(products, min_price, max_price)
        return products

    def apply_filters(self,products, filter_param):
        """Фильтр продуктов по хар-кам"""
        combined_queryset = products
        q_set = []

        current_filter = None
        for filter_item in filter_param:
            if current_filter != PropertyValues.objects.get(id=int(filter_item)).propertyid:
                q_set.append([filter_item])
                current_filter = PropertyValues.objects.get(id=int(filter_item)).propertyid
            else:
                q_set[-1].append(filter_item)

        for filter_list in q_set:
            temp_queryset = Products.objects.none()
            for filter_q in filter_list:
                temp_queryset |= Products.objects.filter(characteristicsset__propertyvalueid=int(filter_q))
            combined_queryset &= temp_queryset

        return combined_queryset.distinct()

    def filter_by_price(self,products, min_price, max_price):
        """Фильтр продуктов по цене"""
        products = products.annotate(
            price_with_disc=ExpressionWrapper(
        F('price') - (F('price') * F('discount') / 100),
        output_field=FloatField()
    ))
        if min_price:
            products = products.filter(price_with_disc__gte=min_price)
        if max_price:
            products = products.filter(price_with_disc__lte=max_price)
        return products

    def apply_sorting(self,products, order_by):
        """Сортировка продуктов"""
        if order_by == "new":
            return products.order_by("id")
        if order_by == "cheap":
            return products.order_by("price")
        if order_by == "expensive":
            return products.order_by("-price")
        return products


class CategoryPredictionView(View):
    """Получение категории товаров по запросу пользователя"""
    def get(self, request):
        new_description = request.GET.get('q', '').strip()
        q = request.GET.get('q', '')
        # Предсказываем категорию
        new_vector = vectorizer.transform([new_description])
        predicted_category = model.predict(new_vector)

        # Строим URL с предсказанной категорией
        url = reverse('catalog:catalog', args=[predicted_category[0]])
        return redirect(f"{url}?q={q}")


class ReviewView(LoginRequiredMixin, CreateView):
    template_name = "products/product.html"
    form_class = ReviewForm
    model = Review
    def form_valid(self, form):
        product_id = self.request.POST.get("product_id")
        product = Products.objects.get(pk=product_id)
        form.instance.user = self.request.user
        form.instance.product = product

        form.save()
        return redirect('products:product', product_slug=product.slug)

    def form_invalid(self, form):
        product_id = self.request.POST.get("product_id")
        product = Products.objects.get(pk=product_id)
        return render(self.request, 'products/product.html', {'form': form, 'product':product})

class UpdateReviewView(LoginRequiredMixin, UpdateView):
    template_name = "products/product.html"
    form_class = ReviewForm
    model = Review

    def get_object(self, queryset=None):
        product_id = self.request.POST.get("product_id")
        return Review.objects.filter(user__id=self.request.user.id).filter(product__id=product_id)[0]

    def get_success_url(self) -> str:
        product_id = self.request.POST.get("product_id")
        product = Products.objects.get(pk=product_id)
        return reverse_lazy('products:product', kwargs={'product_slug': product.slug})

    def form_invalid(self, form):
        product_id = self.request.POST.get("product_id")
        product = Products.objects.get(pk=product_id)
        print("Form Errors:")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in field '{field}': {error}")
        return render(self.request, 'products/product.html', {'product':product})
    