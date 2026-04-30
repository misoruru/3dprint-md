from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_customorder'),
    ]

    operations = [
        # Добавляем поле admin_notes к Product
        migrations.AddField(
            model_name='product',
            name='admin_notes',
            field=models.TextField(blank=True, verbose_name='📝 Заметки (только для админа)',
                                   help_text='Ссылки, комментарии, напоминания — видны только в админке'),
        ),
        # Создаём модель ProductAttachment
        migrations.CreateModel(
            name='ProductAttachment',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attach_type', models.CharField(max_length=10, choices=[('file','Файл'),('link','Ссылка')], default='file', verbose_name='Тип')),
                ('title',       models.CharField(max_length=200, verbose_name='Название / описание')),
                ('file',        models.FileField(blank=True, null=True, upload_to='admin_files/', verbose_name='Файл')),
                ('url',         models.URLField(blank=True, verbose_name='Ссылка')),
                ('created_at',  models.DateTimeField(auto_now_add=True)),
                ('product',     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='attachments', to='shop.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Вложение',
                'verbose_name_plural': 'Файлы и ссылки',
                'ordering': ['-created_at'],
            },
        ),
    ]
