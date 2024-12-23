﻿"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from django.db import models   #для комментариев
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


    # обратная связь
from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    city = forms.CharField(label='Ваш город',min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                               choices=[('1', 'Женский'), ('2', 'Мужской')],
                               widget=forms.RadioSelect, initial=1)
    coffee = forms.ChoiceField(label='С какой проблемой Вы столкнулись',
                                choices=(('1', 'техническая проблема'),
                                ('2','длительное время загрузки'),
                                ('3','запутанная структура сайта'),
                                ('4','своя проблема (напишите о ней в поле "Ваши пожелания" ниже)')), initial=1)
    notice = forms.BooleanField(label='Получать новости о нас на e-mail?',
                                required=False)
    email = forms.EmailField(label='Ваш email')
    rating = forms.ChoiceField(label='Оценка сайта', choices=[(i, i) for i in range(1, 6)])
    suggestions = forms.CharField(label='Ваши пожелания', widget=forms.Textarea)
    

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text
# author будет автоматически выбран в зависимости от авторизованного пользователя
# date автоматически добавляется в момент создания записи

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog   #используемая модель
        fields = ('title', 'description', 'content', 'image',)   #заполняемые поля
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': 'Полное содержание', 'image':"Картинка"}


#формы для добавления, редактирования и удаления товаров и заказов
from .models import Product, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'category']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'total_price']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']
