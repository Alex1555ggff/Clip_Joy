from django import forms
from .models import Comment, Video
from django.contrib.auth import get_user_model


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        labels = {
            "text": "",
        }

        widgets = {
            "text": forms.TextInput(attrs={'placeholder': 'Введите свой комментарий'}),
            }
        

class CreateChannelForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['name', 'description', 'logo']

        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Название канала'}),
            "description": forms.Textarea(attrs={
                'placeholder': 'Придумайте описание (не обязательно)'
                }),
            }
        
        labels = {
            'name': 'Название канала',
            'logo': 'Лого канала',
            'description': 'Описание'
        }


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["name", "photo", "video", "description"]

        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Название канала'}),
            "description": forms.Textarea(attrs={
                'placeholder': 'Придумайте описание (не обязательно)'
                }),
            }
        
        labels = {
            'name': 'Название видео',
            'photo': 'Превью',
            'video': 'Видео',
            'description': 'Описание'
        }
