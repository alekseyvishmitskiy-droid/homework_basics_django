from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def _clean_forbidden_words(self, value):
        if value:
            lower_value = value.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in lower_value:
                    raise ValidationError(f'Использование слова "{word}" запрещено в целях безопасности.')
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return self._clean_forbidden_words(name)

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return self._clean_forbidden_words(description)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5 МБ.')


            valid_types = ['image/jpeg', 'image/png']
            if hasattr(image, 'content_type') and image.content_type not in valid_types:
                raise ValidationError('Допускаются только изображения в формате JPEG или PNG.')
        return image
