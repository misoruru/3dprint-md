from django.core.management import BaseCommand
from shop.models import Product

PRODUCTS = [
    dict(slug='dragon-warrior', name='Воин-Дракон', price=349, genre='fantasy', featured=True,
         material='Фотополимерная смола', size='12-15 см', print_time='8-12 часов',
         colors='Серый, Многоцветный',
         description='Эпическая фэнтези-модель воина с детализированной драконьей броней. Идеально для коллекционеров и любителей настольных игр.'),
    dict(slug='cyber-cat', name='Кибер-Кот', price=299, genre='scifi', featured=True,
         material='Фотополимерная смола', size='10-12 см', print_time='6-10 часов',
         colors='Серый, Многоцветный, LED подсветка',
         description='Футуристическая модель кибер-кота с возможностью установки LED-подсветки. Современный дизайн с технологическими деталями.'),
    dict(slug='space-explorer', name='Космический Исследователь', price=399, genre='scifi', featured=True,
         material='Фотополимерная смола', size='15-18 см', print_time='10-14 часов',
         colors='Серый, Многоцветный',
         description='Детализированная фигурка астронавта с подвижными деталями. Шарнирные соединения позволяют менять позу.'),
    dict(slug='mystic-wizard', name='Мистический Маг', price=329, genre='fantasy', featured=True,
         material='Фотополимерная смола', size='13-16 см', print_time='9-12 часов',
         colors='Серый, Многоцветный',
         description='Детализированный волшебник с магическими эффектами и развевающейся мантией.'),
    dict(slug='robo-buddy', name='Робо-Друг', price=279, genre='cute', featured=True,
         material='Фотополимерная смола', size='8-10 см', print_time='5-8 часов',
         colors='Серый, Многоцветный',
         description='Милый робот-компаньон с шарнирными соединениями. Идеальный настольный сувенир или подарок.'),
    dict(slug='skull-guardian', name='Страж-Череп', price=349, genre='dark', featured=True,
         material='Фотополимерная смола', size='12-14 см', print_time='8-11 часов',
         colors='Серый, Многоцветный',
         description='Мрачная и детализированная модель стража с черепом. Высокая детализация костей и доспехов.'),
]


class Command(BaseCommand):
    help = 'Заполнить БД начальными продуктами'

    def handle(self, *args, **options):
        for data in PRODUCTS:
            obj, created = Product.objects.get_or_create(slug=data['slug'], defaults=data)
            status = 'Создан' if created else 'Уже есть'
            self.stdout.write(f'  {status}: {obj.name}')
        self.stdout.write(self.style.SUCCESS('Готово!'))
