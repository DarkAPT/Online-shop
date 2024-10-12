from django.shortcuts import render

# Create your views here.
def login(request):

    context = {
        "title": "Вход в аккаунт",
    }

    return render(request, 'users/login.html', context)

def registration(request):

    context = {
        "title": "Регистрация",
    }

    return render(request, 'users/registration.html', context)
