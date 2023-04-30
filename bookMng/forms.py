from django import forms
from django.forms import ModelForm
from .models import Book
from django.views.generic import FormView


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]