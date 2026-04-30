import json
import logging
import urllib.request
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .models import Genre, Product, Order, PortfolioPhoto, CustomOrder

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = '8751850441:AAHZWukYBCACUeonoC0ROASu_cZI7wKcZIA'
TELEGRAM_CHAT_ID   = '1321542961'

def send_telegram(text: str) -> None:
    """Отправляет текстовое сообщение через Telegram Bot API."""
    try:
        url     = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        payload = json.dumps({
            'chat_id':    TELEGRAM_CHAT_ID,
            'text':       text,
            'parse_mode': 'HTML',
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
    except Exception as tg_err:
        logger.error(f'Telegram не отправлен: {tg_err}')


def _tg_multipart(fields: dict, file_field: str, filename: str, file_data: bytes, content_type: str) -> bytes:
    """Собирает multipart/form-data вручную."""
    boundary = b'----TGBoundary1234567890'
    body = b''
    for key, value in fields.items():
        body += b'--' + boundary + b'\r\n'
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        body += str(value).encode('utf-8') + b'\r\n'
    body += b'--' + boundary + b'\r\n'
    body += f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode()
    body += f'Content-Type: {content_type}\r\n\r\n'.encode()
    body += file_data + b'\r\n'
    body += b'--' + boundary + b'--\r\n'
    return body, b'multipart/form-data; boundary=' + boundary


def send_telegram_photo_url(photo_url: str, caption: str) -> None:
    """Отправляет фото по URL (chosen_photo из продуктов)."""
    try:
        # Если URL относительный — просто шлём как текст (нет публичного хоста)
        if not photo_url.startswith('http'):
            send_telegram(caption + f'\n\n🖼 Фото варианта: <code>{photo_url}</code>')
            return
        url     = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
        payload = json.dumps({
            'chat_id':    TELEGRAM_CHAT_ID,
            'photo':      photo_url,
            'caption':    caption,
            'parse_mode': 'HTML',
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
    except Exception as tg_err:
        logger.error(f'Telegram sendPhoto не отправлен: {tg_err}')
        # Фоллбэк — просто текст
        send_telegram(caption)


def send_telegram_file(file_path: str, caption: str) -> None:
    """Отправляет файл с диска через sendDocument (для STL, фото и пр.)."""
    import os, mimetypes
    try:
        if not file_path or not os.path.exists(file_path):
            send_telegram(caption + '\n\n⚠️ Файл не найден на сервере')
            return

        filename     = os.path.basename(file_path)
        mime, _      = mimetypes.guess_type(filename)
        mime         = mime or 'application/octet-stream'
        is_image     = mime.startswith('image/')

        with open(file_path, 'rb') as f:
            file_data = f.read()

        tg_method = 'sendPhoto' if is_image else 'sendDocument'
        url       = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{tg_method}'
        file_field = 'photo' if is_image else 'document'

        fields = {
            'chat_id':    TELEGRAM_CHAT_ID,
            'caption':    caption,
            'parse_mode': 'HTML',
        }
        body, content_type_header = _tg_multipart(fields, file_field, filename, file_data, mime)

        req = urllib.request.Request(url, data=body, headers={'Content-Type': content_type_header.decode()})
        urllib.request.urlopen(req, timeout=30)
    except Exception as tg_err:
        logger.error(f'Telegram sendDocument не отправлен: {tg_err}')
        send_telegram(caption)


def index(request):
    featured  = Product.objects.filter(featured=True).prefetch_related('images', 'genre')
    portfolio = PortfolioPhoto.objects.filter(is_visible=True)
    return render(request, 'index.html', {'featured_products': featured, 'portfolio': portfolio})


def catalog(request):
    products = Product.objects.all().prefetch_related('images', 'genre')
    return render(request, 'catalog.html', {'products': products})


@require_http_methods(['GET'])
def api_products(request):
    products = Product.objects.all().prefetch_related('images', 'genre')
    result = {}
    for p in products:
        images            = [img.image.url for img in p.images.all() if img.image]
        selectable_images = [img.image.url for img in p.images.all() if img.image and img.allow_selection]
        result[p.slug] = {
            'name':             p.name,
            'price':            p.price,
            'genre':            p.genre.slug if p.genre else '',
            'genreName':        p.genre.name if p.genre else '',
            'featured':         p.featured,
            'material':         p.material,
            'size':             p.size,
            'time':             p.print_time,
            'colors':           p.colors,
            'description':      p.description,
            'images':           images,
            'selectableImages': selectable_images,  # фото для выбора покупателем
        }
    return JsonResponse(result)


@require_http_methods(['GET'])
def api_genres(request):
    """Возвращает список всех жанров для фильтров в каталоге"""
    genres = Genre.objects.all()
    result = [{'slug': g.slug, 'name': g.name} for g in genres]
    return JsonResponse(result, safe=False)



@require_http_methods(['GET'])
def api_portfolio(request):
    photos = PortfolioPhoto.objects.filter(is_visible=True)
    result = [
        {'url': p.image.url, 'title': p.title}
        for p in photos if p.image
    ]
    return JsonResponse(result, safe=False)

@csrf_exempt
@require_http_methods(['POST'])
def api_custom_order(request):
    try:
        order_type       = request.POST.get('orderType', '')
        customer_name    = request.POST.get('name', '')
        customer_phone   = request.POST.get('phone', '')
        customer_address = request.POST.get('address', '')
        model_size       = request.POST.get('modelSize', '')
        multicolor_raw   = request.POST.get('multicolor', 'false')
        multicolor       = multicolor_raw in ('true', '1', 'on')
        notes            = request.POST.get('notes', '')
        uploaded_file    = request.FILES.get('file')

        # Автоматический расчёт цены
        _BASE = 200
        _SIZE_EXTRA = {'small': 0, 'medium': 100, 'large': 250, 'xlarge': 0}
        _MC_EXTRA   = 300 if multicolor else 0
        if model_size == 'xlarge':
            total_price = 0  # индивидуальный расчёт
        else:
            total_price = _BASE + _SIZE_EXTRA.get(model_size, 0) + _MC_EXTRA
        try:
            total_price = int(request.POST.get('totalPrice', total_price))
        except (ValueError, TypeError):
            pass

        if not all([order_type, customer_name, customer_phone, customer_address]):
            return JsonResponse({'ok': False, 'error': 'Заполните все обязательные поля'}, status=400)

        order = CustomOrder.objects.create(
            order_type=order_type,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            model_size=model_size,
            multicolor=multicolor,
            notes=notes,
            total_price=total_price,
            source='site',
            uploaded_file=uploaded_file,
        )

        type_labels = {
            'standard':   'Стандарт — готовая 3D модель',
            'premium':    'Премиум — создание по фото',
            'human-copy': 'Эксклюзив — 3D копия человека',
        }

        message = f"""
Новый кастомный заказ #{order.pk} на сайте 3Dprint MD!

━━━━━━━━━━━━━━━━━━━━━━
КЛИЕНТ
━━━━━━━━━━━━━━━━━━━━━━
Имя:     {order.customer_name}
Телефон: {order.customer_phone}
Адрес:   {order.customer_address}

━━━━━━━━━━━━━━━━━━━━━━
ЗАКАЗ
━━━━━━━━━━━━━━━━━━━━━━
Тип:     {type_labels.get(order_type, order_type)}
Размер:  {model_size or 'не указан'}
Файл:    {'загружен' if uploaded_file else 'не загружен'}

━━━━━━━━━━━━━━━━━━━━━━
ПОЖЕЛАНИЯ
━━━━━━━━━━━━━━━━━━━━━━
{notes or 'Нет'}
""".strip()

        try:
            send_mail(
                subject=f'📎 Кастомный заказ #{order.pk} — {type_labels.get(order_type, order_type)}',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ORDER_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
        except Exception as mail_err:
            logger.error(f'Email не отправлен: {mail_err}')

        color_label = 'Разноцветная (+300 MDL, ручная работа)' if multicolor else 'Одноцветная'
        price_text  = f'{total_price} MDL' if total_price else 'Индивидуальный расчёт'
        tg_message = (
            f'🌐 <b>Кастомный заказ #{order.pk} (сайт)</b>\n\n'
            f'<b>Тип:</b> {type_labels.get(order_type, order_type)}\n\n'
            f'<b>👤 Клиент</b>\n'
            f'Имя: {order.customer_name}\n'
            f'Телефон: {order.customer_phone}\n'
            f'Адрес: {order.customer_address}\n\n'
            f'<b>📦 Заказ</b>\n'
            f'Размер: {model_size or "не указан"}\n'
            f'Покраска: {color_label}\n'
            f'Файл: {"загружен" if uploaded_file else "не загружен"}\n'
            f'Цена: {price_text}\n\n'
            f'<b>💬 Пожелания</b>\n{notes or "Нет"}'
        )

        if order.uploaded_file:
            import os
            file_path = os.path.join(settings.MEDIA_ROOT, str(order.uploaded_file))
            send_telegram_file(file_path, tg_message)
        else:
            send_telegram(tg_message)

        return JsonResponse({'ok': True, 'orderId': order.pk})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_order(request):
    try:
        data = json.loads(request.body)
        product = get_object_or_404(Product, slug=data['productKey'])
        order = Order.objects.create(
            product=product,
            customer_name=data['name'],
            customer_phone=data['phone'],
            customer_address=data['address'],
            color=data.get('color', 'gray'),
            fill=data.get('fill', 'lattice'),
            notes=data.get('notes', ''),
            total_price=data['totalPrice'],
            chosen_photo=data.get('chosenPhoto', ''),
        )

        color_label = 'Разноцветный (+150 MDL)' if order.color == 'multicolor' else 'Серый (стандарт)'
        fill_label  = 'Полное заполнение (+100 MDL)' if order.fill == 'solid' else 'Решётка'

        message = f"""
Новый заказ #{order.pk} на сайте 3Dprint MD!

━━━━━━━━━━━━━━━━━━━━━━
КЛИЕНТ
━━━━━━━━━━━━━━━━━━━━━━
Имя:     {order.customer_name}
Телефон: {order.customer_phone}
Адрес:   {order.customer_address}

━━━━━━━━━━━━━━━━━━━━━━
ЗАКАЗ
━━━━━━━━━━━━━━━━━━━━━━
Продукт:    {product.name}
Выбранное фото: {order.chosen_photo or 'не выбрано'}
Цвет:       {color_label}
Заполнение: {fill_label}
Итого:      {order.total_price} MDL

━━━━━━━━━━━━━━━━━━━━━━
ПОЖЕЛАНИЯ
━━━━━━━━━━━━━━━━━━━━━━
{order.notes or 'Нет'}
""".strip()

        try:
            send_mail(
                subject=f'🛒 Новый заказ #{order.pk} — {product.name} ({order.total_price} MDL)',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ORDER_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
        except Exception as mail_err:
            logger.error(f'Email не отправлен: {mail_err}')

        tg_message = (
            f'🛒 <b>Новый заказ #{order.pk}</b>\n\n'
            f'<b>👤 Клиент</b>\n'
            f'Имя: {order.customer_name}\n'
            f'Телефон: {order.customer_phone}\n'
            f'Адрес: {order.customer_address}\n\n'
            f'<b>📦 Заказ</b>\n'
            f'Продукт: {product.name}\n'
            f'Цвет: {color_label}\n'
            f'Заполнение: {fill_label}\n'
            f'Итого: <b>{order.total_price} MDL</b>\n\n'
            f'<b>💬 Пожелания</b>\n{order.notes or "Нет"}'
        )

        if order.chosen_photo:
            # chosen_photo хранит URL вида /media/products/file.jpg — делаем абсолютный
            photo_url = order.chosen_photo
            if not photo_url.startswith('http'):
                # Отправляем файл напрямую с диска
                import os
                file_path = os.path.join(settings.MEDIA_ROOT, photo_url.removeprefix(settings.MEDIA_URL))
                send_telegram_file(file_path, tg_message)
            else:
                send_telegram_photo_url(photo_url, tg_message)
        else:
            send_telegram(tg_message)

        return JsonResponse({'ok': True, 'orderId': order.pk})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)
