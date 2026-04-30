from django.db import models


class Genre(models.Model):
    """Жанр/категория продукта — управляется из админки"""
    slug  = models.SlugField(unique=True, verbose_name='Код (латиницей, без пробелов)')
    name  = models.CharField(max_length=100, verbose_name='Название')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    slug        = models.SlugField(unique=True, verbose_name='Ключ (slug)')
    name        = models.CharField(max_length=200, verbose_name='Название')
    price       = models.IntegerField(verbose_name='Цена (MDL)')
    genre       = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='products', verbose_name='Жанр')
    featured    = models.BooleanField(default=False, verbose_name='На главной')
    material    = models.CharField(max_length=200, verbose_name='Материал')
    size        = models.CharField(max_length=100, verbose_name='Размер')
    print_time  = models.CharField(max_length=100, verbose_name='Время печати')
    colors      = models.CharField(max_length=200, verbose_name='Цвета')
    description  = models.TextField(verbose_name='Описание')
    admin_notes  = models.TextField(blank=True, verbose_name='📝 Заметки (только для админа)', help_text='Ссылки, комментарии, напоминания — видны только в админке')
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-featured', 'name']

    def __str__(self):
        return self.name

    def main_image(self):
        first = self.images.first()
        return first.image if first else None


class ProductImage(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
    image           = models.ImageField(upload_to='products/', verbose_name='Фото')
    order           = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    allow_selection = models.BooleanField(default=False, verbose_name='Можно выбрать',
                                          help_text='Покупатель сможет выбрать этот вариант при заказе')

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продукта'
        ordering = ['order']

    def __str__(self):
        return f'Фото #{self.order} — {self.product.name}'



class ProductAttachment(models.Model):
    """Файлы и ссылки — только для админа, на сайте не показываются"""
    TYPE_CHOICES = [
        ('file', 'Файл'),
        ('link', 'Ссылка'),
    ]
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attachments', verbose_name='Продукт')
    attach_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='file', verbose_name='Тип')
    title       = models.CharField(max_length=200, verbose_name='Название / описание')
    file        = models.FileField(upload_to='admin_files/', blank=True, null=True, verbose_name='Файл')
    url         = models.URLField(blank=True, verbose_name='Ссылка')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Файлы и ссылки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.product.name})'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new',        'Новый'),
        ('processing', 'В обработке'),
        ('printing',   'Печатается'),
        ('done',       'Готов'),
        ('delivered',  'Доставлен'),
        ('cancelled',  'Отменён'),
    ]
    product          = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    customer_name    = models.CharField(max_length=200, verbose_name='Имя клиента')
    customer_phone   = models.CharField(max_length=50, verbose_name='Телефон')
    customer_address = models.TextField(verbose_name='Адрес доставки')
    color            = models.CharField(max_length=100, verbose_name='Цвет')
    fill             = models.CharField(max_length=100, verbose_name='Заполнение')
    notes            = models.TextField(blank=True, verbose_name='Пожелания')
    chosen_photo     = models.CharField(max_length=500, blank=True, verbose_name='Выбранное фото (URL)')
    total_price      = models.IntegerField(verbose_name='Итого (MDL)')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.customer_name} ({self.product.name})'


class PortfolioPhoto(models.Model):
    image       = models.ImageField(upload_to='portfolio/', verbose_name='Фото')
    title       = models.CharField(max_length=200, blank=True, verbose_name='Подпись (необязательно)')
    order       = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_visible  = models.BooleanField(default=True, verbose_name='Показывать на сайте')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фото портфолио'
        verbose_name_plural = 'Портфолио'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or f'Фото #{self.pk}'


class CustomOrder(models.Model):
    TYPE_CHOICES = [
        ('standard',   'Стандарт — готовая 3D модель'),
        ('premium',    'Премиум — создание по фото'),
        ('human-copy', 'Эксклюзив — 3D копия человека'),
    ]
    STATUS_CHOICES = [
        ('new',        'Новый'),
        ('processing', 'В обработке'),
        ('printing',   'Печатается'),
        ('done',       'Готов'),
        ('delivered',  'Доставлен'),
        ('cancelled',  'Отменён'),
    ]
    order_type       = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип заказа')
    customer_name    = models.CharField(max_length=200, verbose_name='Имя клиента')
    customer_phone   = models.CharField(max_length=50, verbose_name='Телефон')
    customer_address = models.TextField(verbose_name='Адрес доставки')
    model_size       = models.CharField(max_length=50, blank=True, verbose_name='Размер модели')
    multicolor       = models.BooleanField(default=False, verbose_name='Разноцветная печать')
    notes            = models.TextField(blank=True, verbose_name='Пожелания')
    chosen_photo     = models.CharField(max_length=500, blank=True, verbose_name='Выбранное фото (URL)')
    uploaded_file    = models.FileField(upload_to='custom_orders/', blank=True, null=True, verbose_name='Загруженный файл')
    total_price      = models.IntegerField(default=0, verbose_name='Итого (MDL)')
    source           = models.CharField(max_length=20, default='site', verbose_name='Источник заказа',
                                        help_text='site или telegram')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Кастомный заказ'
        verbose_name_plural = 'Кастомные заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Кастомный заказ #{self.pk} — {self.customer_name} ({self.get_order_type_display()})'
