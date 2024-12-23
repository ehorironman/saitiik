"""
Definition of models.
"""

from email.policy import default
from pyexpat import model
from tabnanny import verbose
from django.db import models

# Create your models here.

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Blog(models. Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    #Методы класса:
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self): #метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title
    #Метаданные - вложенный класс, который задает дополнительные параметры модели
    class Meta:
        db_table = "Posts" #имя таблицы для модели
        ordering = ["-posted"] #порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # тоже для всех статей блога
admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")

    # Методы класса:
    def __str__(self): #метод возвращает название, используемое для представления отдельных записей в административном разделе
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    # Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
admin.site.register(Comment)



#для товаров:
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Stoves', 'Печи'),
        ('Boilers', 'Котлы'),
        ('Barbecues', 'Мангалы'),
        ('Smokers', 'Коптильни'),
        ('Stairs', 'Лестницы'),
        ('Railings', 'Перила'),
        ('Benches', 'Скамейки'),
        ('Tables', 'Столы'),
    ]

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=1, verbose_name="Цена")
    image = models.FileField(upload_to='products/', verbose_name="Изображение")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

admin.site.register(Product)

#для заказов:
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    #user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=1, default=0.00, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    def update_total_price(self):
        self.total_price = sum(item.quantity * item.price for item in self.orderitem_set.all())
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


admin.site.register(Order)

#для товаров в заказе:
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    price = models.DecimalField(max_digits=10, decimal_places=1, default=0.00, verbose_name="Цена")

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказа"


admin.site.register(OrderItem)