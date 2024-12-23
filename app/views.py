"""
Definition of views.
"""

from datetime import datetime
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm #использование встроенной формы регистрации 
from django.shortcuts import render, redirect, get_object_or_404

from django.db import models  #для блога
from .models import Blog #блог

from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария

from .forms import BlogForm # код импорта формы для ввода статьи блога

from .forms import ProductForm, OrderForm, OrderItemForm

from .models import Product, Order, OrderItem

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

#для Полезные ресурсы
def links(request):
    return render(request, 'app/links.html')


#для Обратная связь
from .forms import FeedbackForm #Обратная связь

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Женщина', '2': 'Мужчина'}
    coffee = {'1': 'каждый день', '2': 'несколько раз в день',
              '3': 'несколько раз в неделю', '4': 'несколько раз в месяц'}
    rating = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5' }
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['coffee'] = coffee[form.cleaned_data['coffee'] ]
            data['gender'] = gender[form.cleaned_data['gender'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['rating'] = rating[form.cleaned_data['rating'] ]
            data['suggestions'] = form.cleaned_data['suggestions']
            form = None
    else:
        form = FeedbackForm()
    return render(
        request,
        'app/pool.html',
        {
            'form':form,
            'data': data
         }
    )

#метод действия контроллера registration 
#для обработки данных и передачи данных с сервера 
#для отображения шаблона веб-страницы регистрации

def registration(request):
    """Renders the registration page."""

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы

            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы

            'year':datetime.now().year,
        }
    )



# код метода действия контроллера def newpost(request): 
def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()    # сохраняем изменения после добавления полей

            return redirect('blog')    # переадресация на страницу Блог после создания статьи Блога
    else:
        blogform = BlogForm()     # создание объекта формы для ввода данных

    return render(
        request,
        'app/newpost.html',
        {
            
            'blogform': blogform,     # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )


#для каталога товаров:
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.core.paginator import Paginator
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

def catalog(request):
    query = request.GET.get('search')
    category = request.GET.get('category')

    if query:
        products = Product.objects.filter(title__icontains=query)
    elif category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Пагинация
    paginator = Paginator(products, 20)  # Показывать 20 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
    }

    # Логирование
    logger.info(f"Catalog view accessed with query: {query}, category: {category}")

    return render(request, 'app/catalog.html', context)


#для корзины:
@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, status='new')
    order_items = OrderItem.objects.filter(order=order)
    #OrderItem.objects.filter(order=order).delete()
    #messages.success(request, 'Ваш заказ успешно оформлен.')
    return render(request, 'app/cart.html', {'order': order, 'order_items': order_items})

#для страницы "Мои заказы":
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/my_orders.html', {'orders': orders})

#для административной страницы "Заказы":
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'app/admin_orders.html', {'orders': orders})


@login_required
def checkout(request):
    # Логика для оформления заказа
    return render(request, 'app/checkout.html')


from django.contrib import messages

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status='new')
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    #order_item.quantity += 1
    order_item.quantity = 1
    order_item.price = product.price
    order_item.save()
    order.update_total_price()
    messages.success(request, f'{product.title} добавлен в корзину.')
    return redirect('cart')



@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order = order_item.order
    order_item.delete()
    order.update_total_price()
    return redirect('cart')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = 'cancelled'
    order.save()
    return redirect('my_orders')

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'app/order_details.html', {'order': order, 'order_items': order_items})

@staff_member_required
def admin_cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'cancelled'
    order.save()
    return redirect('admin_orders')

@staff_member_required
def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'app/admin_order_details.html', {'order': order, 'order_items': order_items})


def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()

@login_required
@user_passes_test(is_manager, login_url='login')
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f'Статус заказа {order.id} обновлен.')
        else:
            messages.error(request, 'Неверный статус заказа.')
    return redirect('orders')

@login_required
def orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'STATUS_CHOICES': Order.STATUS_CHOICES,
    }
    return render(request, 'app/admin_orders.html', context)

@login_required
def place_order(request):
    order = Order.objects.filter(user=request.user, status='new').first()
    if order:
        order.status = 'completed'
        order.save()
        # Очистка корзины
        OrderItem.objects.filter(order=order).delete()
        messages.success(request, 'Ваш заказ успешно оформлен.')
    return redirect('checkout')