from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_productimage_allow_selection_order_chosen_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customorder',
            name='chosen_photo',
            field=models.CharField(blank=True, max_length=500, verbose_name='Выбранное фото (URL)'),
        ),
    ]
