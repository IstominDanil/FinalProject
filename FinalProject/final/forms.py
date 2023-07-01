from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Advertisement, Reply, Category


class AdForm(forms.ModelForm):
    headline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=20,
        max_length=128,
        label='Заголовок'
    )
    text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label='Содержание'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Выберите категорию',
        label='Категория',
    )

    class Meta:
        model = Advertisement
        fields = [
            'headline',
            'text',
            'category',
        ]

        labels = {
            # 'category': _('Категория'),
        }

    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get("headline")
        text = cleaned_data.get("text")

        if headline == text:
            raise ValidationError(
                "Заголовок не должен быть идентичен содержанию!"
            )
        return cleaned_data


class ReplyForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 3, 'cols': 100}),
        min_length=3,
        label=''
    )

    class Meta:
        model = Reply
        fields = [
            'text',
        ]


class ReplyDeleteForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = []