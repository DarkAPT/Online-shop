from django.shortcuts import render



# Create your views here.
def catalog_gpu(request):

    context = {
        "title": 'Видеокарты',
    }

    return render(request, 'products/catalog-gpu.html', context)


def catalog_cpu(request):

    context = {
        "title": 'Процессоры',
    }

    return render(request, 'products/catalog-cpu.html', context)


def catalog_motherboard(request):

    context = {
        "title": 'Материнские платы',
    }

    return render(request, 'products/catalog-motherboard.html', context)


def catalog_ssd(request):

    context = {
        "title": 'SSD-диски',
    }

    return render(request, 'products/catalog-ssd.html', context)


def catalog_ram(request):

    context = {
        "title": 'Оперативная память',
    }

    return render(request, 'products/catalog-ram.html', context)
