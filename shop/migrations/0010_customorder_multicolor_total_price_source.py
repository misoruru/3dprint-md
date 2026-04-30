from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_customorder_chosen_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customorder',
            name='multicolor',
            field=models.BooleanField(default=False, verbose_name='Разноцветная печать'),
        ),
        migrations.AddField(
            model_name='customorder',
            name='total_price',
            field=models.IntegerField(default=0, verbose_name='Итого (MDL)'),
        ),
        migrations.AddField(
            model_name='customorder',
            name='source',
            field=models.CharField(default='site', max_length=20,
                                   verbose_name='Источник заказа',
                                   help_text='site или telegram'),
        ),
    ]
