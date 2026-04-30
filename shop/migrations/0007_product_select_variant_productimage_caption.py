from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_admin_notes_productattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='select_variant',
            field=models.BooleanField(
                default=False,
                verbose_name='🎨 Покупатель выбирает вариант',
                help_text='Включи если фото показывают разные варианты товара — покупатель должен выбрать один'
            ),
        ),
        migrations.AddField(
            model_name='productimage',
            name='caption',
            field=models.CharField(
                blank=True, max_length=100,
                verbose_name='Название варианта',
                help_text='Например: «Красный дракон» — показывается покупателю при выборе'
            ),
        ),
    ]
