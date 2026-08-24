from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')


        print(f"Новая заявка! Имя: {name}, Телефон: {phone}, Сообщение: {message}")


        success_message = "Данные успешно отправлены!"

    return render(request, 'catalog/contacts.html', {'success_message': success_message})

