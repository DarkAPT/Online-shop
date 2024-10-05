from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from fuzzywuzzy import process
import joblib
from products.models import Products

model = joblib.load('products/models/model.pkl')
vectorizer = joblib.load('products/models/vectorizer.pkl')


def correct_typos(input_query, choices):
    best_match = process.extractOne(input_query, choices)
    return best_match[0] if best_match[1] > 80 else input_query  # Порог 80%

def get_product_names():
    return Products.objects.values_list('name', flat=True)

def q_search(query):
    query = query.strip().replace(" ", "")
    choices = get_product_names()  # Получаем список названий продуктов
    corrected_query = correct_typos(query, choices)  # Исправляем опечатки

    exact_matches = Products.objects.filter(name__icontains=query)

    vector = SearchVector("name", 'description')
    search_query = SearchQuery(corrected_query)  # Используем исправленный запрос
    if exact_matches:
        return exact_matches
    return Products.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gt=0).order_by("-rank")
