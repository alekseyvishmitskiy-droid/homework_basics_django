from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from catalog.models import Product


def home(request):
    products_list = Product.objects.all().order_by('-id')


    latest_products = products_list[:5]
    print("\n--- ПОСЛЕДНИЕ 5 ПРОДУКТОВ В БАЗЕ ДАННЫХ ---")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
    print("-------------------------------------------\n")


    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'catalog/home.html', {'page_obj': page_obj})


def contacts(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f"Новая заявка! Имя: {name}, Телефон: {phone}, Сообщение: {message}")

        success_message = "Данные успешно отправлены!"

    return render(request, 'catalog/contacts.html', {'success_message': success_message})


def product_detail(request, pk):
    """Контроллер для отображения детальной страницы одного товара."""
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'catalog/product_detail.html', {'product': product})


def product_create(request):
    """Контроллер для обработки формы и создания нового товара."""
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')


        Product.objects.create(
            name=name,
            price=price,
            description=description,
            image=image
        )
        return redirect('catalog:home')

    return render(request, 'catalog/product_form.html')
