from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_genre_add_genre_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioPhoto',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image',      models.ImageField(upload_to='portfolio/', verbose_name='Фото')),
                ('title',      models.CharField(blank=True, max_length=200, verbose_name='Подпись (необязательно)')),
                ('order',      models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Фото портфолио',
                'verbose_name_plural': 'Портфолио',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
