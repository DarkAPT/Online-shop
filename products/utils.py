import joblib
from products.models import Products

def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    else:
        return Products.objects.all()


model = joblib.load('products/models/model.pkl')
vectorizer = joblib.load('products/models/vectorizer.pkl')
