from django.shortcuts import render

# Create your views here.
def catalog_gpu(request):
    context = {
        "products":[
            {
                'image': 'products/images/rtx3060 12gm 200x200.webp',
                'name': 'Видеокарта Gigabyte GeForce RTX 3060 EAGLE OC 12G',
                'memory_type': 'GDDR6',
                'memory_size': '12 ГБ',
                'memory_bus_size': '192 бит',
                'memory_bus_type': 'PCI Express 4.0',
                'old_price': '50 000',
                'new_price': '45 000'
            },           
        ]
    }

    return render(request, 'products/catalog-gpu.html', context)


def catalog_cpu(request):

    return render(request, 'products/catalog-cpu.html')


def catalog_motherboard(request):

    return render(request, 'products/catalog-motherboard.html')


def catalog_ssd(request):

    return render(request, 'products/catalog-ssd.html')


def catalog_ram(request):

    return render(request, 'products/catalog-ram.html')
