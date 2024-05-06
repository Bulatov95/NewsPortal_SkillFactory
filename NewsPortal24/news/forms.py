from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'tittle',
            'text_post',
            'category',
            'post_author',
        ]

        def clean(self):
            cleaned_data = super().clean()
            tittle = cleaned_data.get('tittle')
            text_post = cleaned_data.get('text_post')
            if tittle == text_post:
                raise ValidationError(
                    'Текст не должен совпадать с заголовком!'
                )
            return cleaned_data