from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.db.models import F, ExpressionWrapper, FloatField
from products.utils import q_search
from products.models import Products,Properties,PropertyValues
from products.utils import model,vectorizer


# Create your views here.
def product(request, product_slug):
    product_obj = Products.objects.get(slug=product_slug)

    context = {
        "product": product_obj
    }

    return render(request, 'products/product.html' ,context)


def catalog(request, category_slug=None, page=1):
    products = Products.objects.filter(categoryid__slug=category_slug)
    properties = Properties.objects.filter(categoryid__slug=category_slug)
    query = request.GET.get('q', None)

    if query:
        products = q_search(query)
    if products:
        title = products[0].categoryid.name
    else:
        title = "Каталог"

    paginator = Paginator(products,4)
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

    if query:
        products = q_search(query)
    else:
        products = Products.objects.filter(categoryid__slug=category_slug)
    # Если есть параметр фильтра, применяем фильтрацию к товарам
    if filter_param:
        prop_list = []
        if not query:
            combined_queryset = Products.objects.none()
        else:
            combined_queryset = q_search(query)
        for filter_item in filter_param:
            filter_property_id = PropertyValues.objects.get(id=int(filter_item)).propertyid
            if filter_property_id in prop_list:
                combined_queryset = combined_queryset | Products.objects.filter(characteristicsset__propertyvalueid=int(filter_item))
            elif not combined_queryset.exists():
                combined_queryset = combined_queryset | Products.objects.filter(characteristicsset__propertyvalueid=int(filter_item))
                prop_list.append(filter_property_id)
            else:
                prop_list.append(filter_property_id)
                combined_queryset = combined_queryset & Products.objects.filter(characteristicsset__propertyvalueid=int(filter_item))
        products = combined_queryset.distinct()

    if order_by:
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
        paginator = Paginator(products,4)
        current_page = paginator.page(1)

        data = render_to_string('products/async/catalog.html', {'products':current_page})
    else:
        data = render_to_string('products/async/not_found_page.html')
    return JsonResponse({"data": data})


def products_ordering(request):
    order_by = request.GET.get('action')
    redirect('filter-product', order = order_by)


def category_prediction(request):
    new_description = request.GET.get('q', '').strip()
    new_vector = vectorizer.transform([new_description])
    predicted_category = model.predict(new_vector)
    url = reverse('catalog:catalog', args=[predicted_category[0]])
    return redirect(url)