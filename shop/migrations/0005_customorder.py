from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_portfoliophoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('id',               models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type',       models.CharField(max_length=20, choices=[('standard','Стандарт — готовая 3D модель'),('premium','Премиум — создание по фото'),('human-copy','Эксклюзив — 3D копия человека')], verbose_name='Тип заказа')),
                ('customer_name',    models.CharField(max_length=200, verbose_name='Имя клиента')),
                ('customer_phone',   models.CharField(max_length=50, verbose_name='Телефон')),
                ('customer_address', models.TextField(verbose_name='Адрес доставки')),
                ('model_size',       models.CharField(blank=True, max_length=50, verbose_name='Размер модели')),
                ('notes',            models.TextField(blank=True, verbose_name='Пожелания')),
                ('uploaded_file',    models.FileField(blank=True, null=True, upload_to='custom_orders/', verbose_name='Загруженный файл')),
                ('status',           models.CharField(max_length=20, choices=[('new','Новый'),('processing','В обработке'),('printing','Печатается'),('done','Готов'),('delivered','Доставлен'),('cancelled','Отменён')], default='new', verbose_name='Статус')),
                ('created_at',       models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
            ],
            options={
                'verbose_name': 'Кастомный заказ',
                'verbose_name_plural': 'Кастомные заказы',
                'ordering': ['-created_at'],
            },
        ),
    ]
