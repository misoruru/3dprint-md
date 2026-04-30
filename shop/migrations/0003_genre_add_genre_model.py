from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_product_emoji_remove_product_image_and_more'),
    ]

    operations = [
        # 1. Создаём модель Genre
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id',    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug',  models.SlugField(unique=True, verbose_name='Код (латиницей, без пробелов)')),
                ('name',  models.CharField(max_length=100, verbose_name='Название')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ['order', 'name'],
            },
        ),
        # 2. Добавляем временное поле genre_new (FK, null разрешён)
        migrations.AddField(
            model_name='product',
            name='genre_new',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='products',
                to='shop.genre',
                verbose_name='Жанр',
            ),
        ),
        # 3. Удаляем старое поле genre (CharField)
        migrations.RemoveField(
            model_name='product',
            name='genre',
        ),
        # 4. Переименовываем genre_new → genre
        migrations.RenameField(
            model_name='product',
            old_name='genre_new',
            new_name='genre',
        ),
    ]
