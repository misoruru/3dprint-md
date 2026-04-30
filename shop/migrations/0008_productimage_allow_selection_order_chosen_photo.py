from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # Наша предыдущая миграция
        ('shop', '0006_product_admin_notes_productattachment'),
        # Миграция пользователя которая уже была на его машине
        ('shop', '0007_product_select_variant_productimage_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='allow_selection',
            field=models.BooleanField(default=False, verbose_name='Можно выбрать',
                                      help_text='Покупатель сможет выбрать этот вариант при заказе'),
        ),
        migrations.AddField(
            model_name='order',
            name='chosen_photo',
            field=models.CharField(blank=True, max_length=500, verbose_name='Выбранное фото (URL)'),
        ),
    ]
