from django.shortcuts import render
from catalog.models import Product


def home(request):
    latest_products = Product.objects.all()[:5]


    print("\n--- ПОСЛЕДНИЕ 5 ПРОДУКТОВ В БАЗЕ ДАННЫХ ---")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
    print("-------------------------------------------\n")


    return render(request, 'catalog/home.html', {'products': latest_products})


def contacts(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f"Новая заявка! Имя: {name}, Телефон: {phone}, Сообщение: {message}")

        success_message = "Данные успешно отправлены!"

    return render(request, 'catalog/contacts.html', {'success_message': success_message})


