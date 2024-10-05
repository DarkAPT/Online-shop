from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.db.models import F, ExpressionWrapper, FloatField
from products.utils import q_search
from products.models import Products,Properties,PropertyValues,Categories
from products.utils import model,vectorizer


# Create your views here.
def product(request, product_slug):
    product_obj = Products.objects.get(slug=product_slug)

    context = {
        "product": product_obj
    }

    return render(request, 'products/product.html' ,context)


def catalog(request, category_slug, page=1):

    properties = Properties.objects.filter(categoryid__slug=category_slug)
    title = Categories.objects.filter(slug = category_slug)[0].name

    query = request.GET.get('q', None)


    if query:
        products = q_search(query)
        products = products.filter(categoryid__slug=category_slug)
    else:
        products = Products.objects.filter(categoryid__slug=category_slug)

    paginator = Paginator(products,1)
    current_page = paginator.page(page)

    context = {
        "title": title,
        "products": current_page,
        "properties": properties,
        "category_slug": category_slug,
    }

    return render(request, 'products/catalog.html', context)


def filter_product(request):
    filter_param = request.GET.getlist('filter[]')
    if 'order_by' in request.GET:
        order_by = request.GET['order_by']
    else:
        order_by = 'new'

    category_slug = request.GET.get('category_slug')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    query = request.GET.get('q', None)
    page = request.GET.get('page')

    if query:
        products = q_search(query)
    else:
        products = Products.objects.filter(categoryid__slug=category_slug)
    # Если есть параметр фильтра, применяем фильтрацию к товарам
    if filter_param:
        combined_queryset = products
        q_set = []

        current_filter = None
        for filter_item in filter_param:
            if current_filter != PropertyValues.objects.get(id=int(filter_item)).propertyid:
                q_set.append([filter_item])
                current_filter = PropertyValues.objects.get(id=int(filter_item)).propertyid
            else:
                q_set[-1].append(filter_item)

        temp_queryset = Products.objects.none()
        for filter_list in q_set:
            for filter_q in filter_list:
                temp_queryset |= Products.objects.filter(characteristicsset__propertyvalueid=int(filter_q))
            combined_queryset &= temp_queryset
            temp_queryset = Products.objects.none()

        products = combined_queryset.distinct()

    if order_by == "new":
        products = products.order_by("id")
    elif order_by == "cheap":
        products = products.order_by("price")
    elif order_by == "expensive":
        products = products.order_by("-price")

    if min_price or max_price:
        products = products.annotate(
            price_with_disc=ExpressionWrapper(
        F('price') - (F('price') * F('discount') / 100),
        output_field=FloatField()
    )).filter(price_with_disc__gte=min_price).filter(price_with_disc__lte=max_price)

    if products:
        paginator = Paginator(products,1)
        current_page = paginator.page(page)

        data = render_to_string('products/async/catalog.html', {'products':current_page})
    else:
        data = render_to_string('products/async/not_found_page.html')
    return JsonResponse({"data": data})


def products_ordering(request):
    order_by = request.GET.get('action')
    redirect('filter-product', order = order_by)


def category_prediction(request):
    new_description = request.GET.get('q', '').strip()
    q = request.GET.get('q', '')
    new_vector = vectorizer.transform([new_description])
    predicted_category = model.predict(new_vector)
    url = reverse('catalog:catalog', args=[predicted_category[0]])
    return redirect(f"{url}?q={q}")
