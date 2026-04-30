"""
Telegram-бот для 3Dprint MD
Запуск: python telegram_bot.py (из папки с manage.py, при активном venv)

Требует: pip install pyTelegramBotAPI django
Перед запуском: export DJANGO_SETTINGS_MODULE=config.settings
"""

import os
import sys
import django

# ── Django setup ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
# ────────────────────────────────────────────────────────────────────────────

import telebot
from telebot import types
from shop.models import CustomOrder
from shop.views import send_telegram, send_telegram_file

BOT_TOKEN        = '8751850441:AAHZWukYBCACUeonoC0ROASu_cZI7wKcZIA'
ADMIN_ID         = 1321542961
SITE_URL         = 'https://3dprint-md.com'   # замени на реальный адрес

BASE_PRICE       = 200
SIZE_EXTRA       = {'small': 0, 'medium': 100, 'large': 250, 'xlarge': None}
MULTICOLOR_EXTRA = 300

SIZE_LABELS = {
    'small':  'Маленький (до 5 см)',
    'medium': 'Средний (5–10 см) +100 MDL',
    'large':  'Большой (10–15 см) +250 MDL',
    'xlarge': 'Очень большой (15 см+) — инд. расчёт',
}
TYPE_LABELS = {
    'standard':   '📦 Готовая 3D модель',
    'premium':    '🖼 Создание по фото',
    'human-copy': '🧍 3D копия человека',
}
STATUS_LABELS = {
    'new':        '🆕 Новый',
    'processing': '🔄 В обработке',
    'printing':   '🖨 Печатается',
    'done':       '✅ Готов',
    'delivered':  '📦 Доставлен',
    'cancelled':  '❌ Отменён',
}

bot = telebot.TeleBot(BOT_TOKEN)

# state[uid] = {'step': str, 'msg_id': int|None, 'data': dict}
state: dict = {}


# ── Хелперы состояния ────────────────────────────────────────────────────────

def gs(uid):
    return state.get(uid, {'step': None, 'msg_id': None, 'data': {}})

def ss(uid, step, msg_id=None, **kwargs):
    if uid not in state:
        state[uid] = {'step': None, 'msg_id': None, 'data': {}}
    state[uid]['step'] = step
    if msg_id is not None:
        state[uid]['msg_id'] = msg_id
    state[uid]['data'].update(kwargs)

def clear(uid):
    state.pop(uid, None)

def is_admin(uid):
    return uid == ADMIN_ID


# ── edit_or_send ─────────────────────────────────────────────────────────────

def edit_or_send(uid, text, kb=None, parse_mode='HTML'):
    """Редактирует сохранённое сообщение или шлёт новое. Возвращает message_id."""
    s   = gs(uid)
    mid = s.get('msg_id')
    if mid:
        try:
            m = bot.edit_message_text(
                text, chat_id=uid, message_id=mid,
                parse_mode=parse_mode, reply_markup=kb,
            )
            return m.message_id
        except Exception:
            pass
    m = bot.send_message(uid, text, parse_mode=parse_mode, reply_markup=kb)
    return m.message_id


# ── ГЛАВНОЕ МЕНЮ ─────────────────────────────────────────────────────────────

def show_main_menu(uid, call=None):
    if is_admin(uid):
        text = '🔧 <b>Панель администратора</b>\n\nВыберите раздел:'
        kb   = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton('📋 Все заказы',    callback_data='admin_orders_all'),
            types.InlineKeyboardButton('🆕 Новые',         callback_data='admin_orders_new'),
            types.InlineKeyboardButton('🔄 В обработке',  callback_data='admin_orders_processing'),
            types.InlineKeyboardButton('🖨 Печатаются',   callback_data='admin_orders_printing'),
            types.InlineKeyboardButton('✅ Готовые',       callback_data='admin_orders_done'),
        )
    else:
        text = (
            '👋 Привет! Это бот <b>3Dprint MD</b> — печать 3D моделей на заказ (DLP принтер).\n\n'
            '💳 Оплата при получении\n\n'
            'Выберите тип заказа:'
        )
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton('  📦  У меня есть готовый файл  ',    callback_data='order_standard'),
            types.InlineKeyboardButton('  🖼  Создать модель по фото  ',       callback_data='order_premium'),
            types.InlineKeyboardButton('  🧍  3D фигурка по фото человека  ',  callback_data='order_human'),
            types.InlineKeyboardButton('  🌐  Каталог и примеры работ  ',      url=SITE_URL),
            types.InlineKeyboardButton('  💬  Связаться с мастером  ',         url='https://t.me/misoruru'),
        )

    if call:
        try:
            bot.edit_message_text(text, chat_id=uid, message_id=call.message.message_id,
                                  parse_mode='HTML', reply_markup=kb)
            ss(uid, 'menu', msg_id=call.message.message_id)
            return
        except Exception:
            pass

    m = bot.send_message(uid, text, parse_mode='HTML', reply_markup=kb)
    ss(uid, 'menu', msg_id=m.message_id)


# ── КОМАНДЫ ──────────────────────────────────────────────────────────────────

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(msg):
    clear(msg.from_user.id)
    show_main_menu(msg.from_user.id)

@bot.message_handler(commands=['cancel'])
def cmd_cancel(msg):
    uid = msg.from_user.id
    clear(uid)
    show_main_menu(uid)


# ── ШАГИ ОФОРМЛЕНИЯ ЗАКАЗА ───────────────────────────────────────────────────

def _cancel_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('❌ Отмена', callback_data='cancel_order'))
    return kb

def show_step_await_file(uid):
    m = bot.send_message(
        uid,
        '📦 <b>Шаг 1 из 6 — Файл модели</b>\n\n'
        'Отправьте файл вашей 3D модели (STL, OBJ и т.д.).',
        parse_mode='HTML', reply_markup=_cancel_kb(),
    )
    ss(uid, 'await_file', msg_id=m.message_id)

def show_step_await_photo_premium(uid):
    m = bot.send_message(
        uid,
        '🖼 <b>Шаг 1 из 6 — Фото объекта</b>\n\n'
        'Отправьте фотографию объекта, который нужно воссоздать в 3D.',
        parse_mode='HTML', reply_markup=_cancel_kb(),
    )
    ss(uid, 'await_photo_premium', msg_id=m.message_id)

def show_step_await_photos_human(uid, count=0):
    kb = types.InlineKeyboardMarkup(row_width=1)
    if count > 0:
        kb.add(types.InlineKeyboardButton(f'✅ Готово — у меня {count} фото', callback_data='photos_done'))
    kb.add(types.InlineKeyboardButton('❌ Отмена', callback_data='cancel_order'))
    text = (
        f'🧍 <b>Шаг 1 из 6 — Фото человека</b>\n\n'
        f'Отправьте <b>3–5 фотографий</b> в полный рост (желательно со всех сторон).\n\n'
        f'Получено: <b>{count}</b> из 5'
    )
    s   = gs(uid)
    mid = s.get('msg_id')
    try:
        if mid and count > 0:
            bot.edit_message_text(text, chat_id=uid, message_id=mid,
                                  parse_mode='HTML', reply_markup=kb)
            return
    except Exception:
        pass
    m = bot.send_message(uid, text, parse_mode='HTML', reply_markup=kb)
    ss(uid, 'await_photos_human', msg_id=m.message_id)

def show_step_name(uid):
    new_mid = edit_or_send(uid, '👤 <b>Шаг 2 из 6 — Ваше имя</b>\n\nВведите ваше имя:', kb=_cancel_kb())
    ss(uid, 'await_name', msg_id=new_mid)

def show_step_phone(uid):
    new_mid = edit_or_send(uid, '📞 <b>Шаг 3 из 6 — Номер телефона</b>\n\nВведите ваш номер телефона:', kb=_cancel_kb())
    ss(uid, 'await_phone', msg_id=new_mid)

def show_step_address(uid):
    new_mid = edit_or_send(uid, '🏠 <b>Шаг 4 из 6 — Адрес доставки</b>\n\nВведите адрес доставки:', kb=_cancel_kb())
    ss(uid, 'await_address', msg_id=new_mid)

def show_step_size(uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton('📏 Маленький (до 5 см)     — базовая цена', callback_data='size_small'),
        types.InlineKeyboardButton('📏 Средний (5–10 см)       — +100 MDL',     callback_data='size_medium'),
        types.InlineKeyboardButton('📏 Большой (10–15 см)      — +250 MDL',     callback_data='size_large'),
        types.InlineKeyboardButton('📏 Очень большой (15 см+)  — инд. расчёт', callback_data='size_xlarge'),
        types.InlineKeyboardButton('❌ Отмена', callback_data='cancel_order'),
    )
    new_mid = edit_or_send(uid, '📐 <b>Шаг 5 из 6 — Размер модели</b>\n\nВыберите размер:', kb=kb)
    ss(uid, 'await_size', msg_id=new_mid)

def show_step_multicolor(uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton('⬜ Одноцветная  — стандарт',                               callback_data='color_mono'),
        types.InlineKeyboardButton(f'🎨 Разноцветная — +{MULTICOLOR_EXTRA} MDL, ручная работа', callback_data='color_multi'),
        types.InlineKeyboardButton('❌ Отмена', callback_data='cancel_order'),
    )
    new_mid = edit_or_send(
        uid,
        '🎨 <b>Шаг 6 из 6 — Покраска</b>\n\n'
        '⚠️ Разноцветная — ручная роспись, существенно увеличивает стоимость.',
        kb=kb,
    )
    ss(uid, 'await_multicolor', msg_id=new_mid)

def show_step_notes(uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton('➡️ Пропустить', callback_data='notes_skip'),
        types.InlineKeyboardButton('❌ Отмена',      callback_data='cancel_order'),
    )
    new_mid = edit_or_send(uid, '💬 <b>Особые пожелания</b>\n\nВведите текст или нажмите «Пропустить»:', kb=kb)
    ss(uid, 'await_notes', msg_id=new_mid)

def show_summary(uid):
    s  = gs(uid)
    d  = s['data']
    size       = d.get('size', 'small')
    multicolor = d.get('multicolor', False)
    order_type = d.get('order_type', '')

    if size == 'xlarge':
        price       = None
        total_price = 0
    else:
        extra       = (SIZE_EXTRA.get(size) or 0)
        mc          = MULTICOLOR_EXTRA if multicolor else 0
        price       = BASE_PRICE + extra + mc
        total_price = price

    ss(uid, 'await_confirm', total_price=total_price)

    size_str  = SIZE_LABELS.get(size, size)
    color_str = f'🎨 Разноцветная (+{MULTICOLOR_EXTRA} MDL)' if multicolor else '⬜ Одноцветная'
    type_str  = TYPE_LABELS.get(order_type, order_type)
    price_str = f'<b>{price} MDL</b>' if price else '<b>Индивидуальный расчёт</b>\n(мастер свяжется с вами)'

    text = (
        f'📋 <b>Ваш заказ — проверьте детали</b>\n\n'
        f'Тип: {type_str}\n'
        f'Имя: {d.get("name", "")}\n'
        f'Телефон: {d.get("phone", "")}\n'
        f'Адрес: {d.get("address", "")}\n'
        f'Размер: {size_str}\n'
        f'Покраска: {color_str}\n'
        f'Пожелания: {d.get("notes") or "—"}\n\n'
        f'💰 Итого: {price_str}\n'
        f'💳 Оплата при получении\n\n'
        f'Всё верно? Подтвердить заказ?'
    )
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirm_order'),
        types.InlineKeyboardButton('❌ Отмена',      callback_data='cancel_order'),
    )
    new_mid = edit_or_send(uid, text, kb=kb)
    ss(uid, 'await_confirm', msg_id=new_mid)


# ── CALLBACK ─────────────────────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda c: True)
def on_callback(call: types.CallbackQuery):
    uid  = call.from_user.id
    data = call.data
    bot.answer_callback_query(call.id)

    # Тип заказа
    if data == 'order_standard':
        clear(uid)
        ss(uid, 'menu', order_type='standard')
        show_step_await_file(uid)

    elif data == 'order_premium':
        clear(uid)
        ss(uid, 'menu', order_type='premium')
        show_step_await_photo_premium(uid)

    elif data == 'order_human':
        clear(uid)
        ss(uid, 'menu', order_type='human-copy', photos=[])
        show_step_await_photos_human(uid, count=0)

    elif data == 'photos_done':
        s      = gs(uid)
        photos = s['data'].get('photos', [])
        if not photos:
            bot.answer_callback_query(call.id, '⚠️ Сначала отправьте хотя бы одно фото!', show_alert=True)
        else:
            show_step_name(uid)

    # Размер
    elif data.startswith('size_'):
        size = data.split('_', 1)[1]
        ss(uid, 'await_multicolor', size=size)
        show_step_multicolor(uid)

    # Покраска
    elif data == 'color_mono':
        ss(uid, 'await_notes', multicolor=False)
        show_step_notes(uid)
    elif data == 'color_multi':
        ss(uid, 'await_notes', multicolor=True)
        show_step_notes(uid)

    elif data == 'notes_skip':
        ss(uid, 'await_confirm', notes='')
        show_summary(uid)

    # Подтверждение
    elif data == 'confirm_order':
        finalize_order(uid, call)

    elif data == 'cancel_order':
        clear(uid)
        show_main_menu(uid, call)

    elif data == 'back_to_menu':
        clear(uid)
        show_main_menu(uid, call)

    # Админка
    elif data.startswith('admin_orders_'):
        if not is_admin(uid): return
        status_filter = data.replace('admin_orders_', '')
        show_admin_orders(uid, call, status_filter)

    elif data.startswith('admin_setstatus_'):
        if not is_admin(uid): return
        # callback format: admin_setstatus_{order_id}_{status}
        # split only into 4 parts to handle statuses with underscores
        _, _, order_id_str, new_status = data.split('_', 3)
        admin_set_status(uid, call, int(order_id_str), new_status)

    elif data.startswith('admin_order_'):
        if not is_admin(uid): return
        order_id = int(data.replace('admin_order_', ''))
        show_admin_order_detail(uid, call, order_id)

    elif data == 'back_admin_menu':
        if not is_admin(uid): return
        show_main_menu(uid, call)


# ── ВХОДЯЩИЕ ФАЙЛЫ И ФОТО ────────────────────────────────────────────────────

@bot.message_handler(content_types=['document'])
def on_document(msg):
    uid = msg.from_user.id
    s   = gs(uid)
    if s.get('step') == 'await_file':
        file_id = msg.document.file_id
        fname   = msg.document.file_name
        try: bot.delete_message(uid, msg.message_id)
        except Exception: pass
        ss(uid, 'await_name', uploaded_file_id=file_id, uploaded_file_name=fname)
        show_step_name(uid)
        # Маленькое всплывающее подтверждение через edit
        try:
            s2 = gs(uid)
            mid = s2.get('msg_id')
            if mid:
                cur = bot.edit_message_text(
                    f'✅ <b>Файл «{fname}» получен!</b>\n\n'
                    '👤 <b>Шаг 2 из 6 — Ваше имя</b>\n\nВведите ваше имя:',
                    chat_id=uid, message_id=mid,
                    parse_mode='HTML', reply_markup=_cancel_kb(),
                )
        except Exception:
            pass
    else:
        bot.send_message(uid, '⚠️ Сейчас файл не нужен. Нажмите /menu для начала.')


@bot.message_handler(content_types=['photo'])
def on_photo(msg):
    uid  = msg.from_user.id
    s    = gs(uid)
    step = s.get('step', '')

    if step == 'await_photo_premium':
        file_id = msg.photo[-1].file_id
        try: bot.delete_message(uid, msg.message_id)
        except Exception: pass
        ss(uid, 'await_name', uploaded_file_id=file_id, uploaded_file_name='photo.jpg')
        show_step_name(uid)
        try:
            s2  = gs(uid)
            mid = s2.get('msg_id')
            if mid:
                bot.edit_message_text(
                    '✅ <b>Фото получено!</b>\n\n'
                    '👤 <b>Шаг 2 из 6 — Ваше имя</b>\n\nВведите ваше имя:',
                    chat_id=uid, message_id=mid,
                    parse_mode='HTML', reply_markup=_cancel_kb(),
                )
        except Exception:
            pass

    elif step == 'await_photos_human':
        photos = s['data'].get('photos', [])
        photos.append(msg.photo[-1].file_id)
        try: bot.delete_message(uid, msg.message_id)
        except Exception: pass
        ss(uid, 'await_photos_human', photos=photos)
        show_step_await_photos_human(uid, count=len(photos))

    else:
        bot.send_message(uid, '⚠️ Фото сейчас не нужно. Нажмите /menu.')


# ── ВХОДЯЩИЙ ТЕКСТ ───────────────────────────────────────────────────────────

@bot.message_handler(content_types=['text'])
def on_text(msg):
    uid  = msg.from_user.id
    text = msg.text.strip()
    s    = gs(uid)
    step = s.get('step', '')

    # Удаляем сообщение пользователя чтобы не засорять чат
    try: bot.delete_message(uid, msg.message_id)
    except Exception: pass

    if step == 'await_name':
        ss(uid, 'await_phone', name=text)
        show_step_phone(uid)
    elif step == 'await_phone':
        ss(uid, 'await_address', phone=text)
        show_step_address(uid)
    elif step == 'await_address':
        ss(uid, 'await_size', address=text)
        show_step_size(uid)
    elif step == 'await_notes':
        ss(uid, 'await_confirm', notes=text)
        show_summary(uid)
    else:
        show_main_menu(uid)


# ── СОЗДАНИЕ ЗАКАЗА ──────────────────────────────────────────────────────────

def finalize_order(uid, call):
    from django.core.files.base import ContentFile
    import urllib.request as ureq

    s = gs(uid)
    d = s['data']

    order_type  = d.get('order_type', 'standard')
    name        = d.get('name', '')
    phone       = d.get('phone', '')
    address     = d.get('address', '')
    size        = d.get('size', 'small')
    multicolor  = d.get('multicolor', False)
    notes       = d.get('notes', '')
    total_price = d.get('total_price', 0)
    file_id     = d.get('uploaded_file_id', '')
    file_name   = d.get('uploaded_file_name', 'upload')
    photos      = d.get('photos', [])

    # Скачиваем файл/фото
    import zipfile, io
    django_file = None
    try:
        if order_type == 'human-copy' and photos:
            # Несколько фото -> архивируем в zip
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i, fid in enumerate(photos, start=1):
                    try:
                        fi  = bot.get_file(fid)
                        ext = fi.file_path.rsplit('.', 1)[-1] if '.' in fi.file_path else 'jpg'
                        url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{fi.file_path}'
                        with ureq.urlopen(url, timeout=20) as r:
                            raw = r.read()
                        zf.writestr(f'photo_{i}.{ext}', raw)
                    except Exception as e:
                        print(f'[BOT] Фото {i} не скачалось: {e}')
            zip_buf.seek(0)
            safe_name = name.replace(' ', '_').replace('/', '-')
            zip_name = f'photos_{safe_name}_order.zip'
            django_file = ContentFile(zip_buf.read(), name=zip_name)
        else:
            # Одиночный файл или фото (standard / premium)
            fid = file_id or (photos[0] if photos else None)
            if fid:
                fi  = bot.get_file(fid)
                url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{fi.file_path}'
                with ureq.urlopen(url, timeout=20) as r:
                    raw = r.read()
                django_file = ContentFile(raw, name=file_name or fi.file_path.split('/')[-1])
    except Exception as e:
        print(f'[BOT] Не удалось скачать файл: {e}')

    order = CustomOrder.objects.create(
        order_type=order_type,
        customer_name=name,
        customer_phone=phone,
        customer_address=address,
        model_size=size,
        multicolor=multicolor,
        notes=notes,
        total_price=total_price,
        source='telegram',
        uploaded_file=django_file,
    )

    size_label  = SIZE_LABELS.get(size, size)
    color_label = f'Разноцветная (+{MULTICOLOR_EXTRA} MDL)' if multicolor else 'Одноцветная'
    type_label  = TYPE_LABELS.get(order_type, order_type)
    price_str   = f'{total_price} MDL' if total_price else 'Индивидуальный расчёт'

    # Финальное сообщение пользователю (редактируем текущее)
    kb_done = types.InlineKeyboardMarkup(row_width=1)
    kb_done.add(
        types.InlineKeyboardButton('🌐 Каталог и примеры работ', url=SITE_URL),
        types.InlineKeyboardButton('🔁 Сделать ещё заказ',        callback_data='back_to_menu'),
    )
    confirm_text = (
        f'🎉 <b>Заказ #{order.pk} принят!</b>\n\n'
        f'Тип: {type_label}\n'
        f'Размер: {size_label}\n'
        f'Покраска: {color_label}\n'
        f'Цена: {price_str}\n\n'
        f'💳 Оплата при получении\n'
        f'Мастер свяжется с вами в ближайшее время.'
    )
    try:
        bot.edit_message_text(
            confirm_text, chat_id=uid, message_id=call.message.message_id,
            parse_mode='HTML', reply_markup=kb_done,
        )
    except Exception:
        bot.send_message(uid, confirm_text, parse_mode='HTML', reply_markup=kb_done)

    # Ссылка на TG профиль клиента
    tg_user = call.from_user
    tg_name = (tg_user.first_name or '') + (' ' + tg_user.last_name if tg_user.last_name else '')
    if tg_user.username:
        tg_link = f'<a href="https://t.me/{tg_user.username}">@{tg_user.username}</a>'
    else:
        tg_link = f'<a href="tg://user?id={tg_user.id}">{tg_name.strip() or "без username"}</a>'

    # Уведомление администратору
    tg_text = (
        f'📲 <b>Новый заказ #{order.pk} (Telegram-бот)</b>\n\n'
        f'<b>👤 Клиент</b>\n'
        f'Имя: {name}\n'
        f'Телефон: {phone}\n'
        f'Адрес: {address}\n'
        f'Telegram: {tg_link}\n\n'
        f'<b>📦 Заказ</b>\n'
        f'Тип: {type_label}\n'
        f'Размер: {size_label}\n'
        f'Покраска: {color_label}\n'
        f'Цена: {price_str}\n\n'
        f'<b>💬 Пожелания</b>\n{notes or "Нет"}'
    )

    from django.conf import settings
    import os
    if order.uploaded_file:
        fp = os.path.join(settings.MEDIA_ROOT, str(order.uploaded_file))
        send_telegram_file(fp, tg_text)
    else:
        send_telegram(tg_text)

    clear(uid)


# ── АДМИН: список заказов ────────────────────────────────────────────────────

def show_admin_orders(uid, call, status_filter='all'):
    if status_filter == 'all':
        qs = CustomOrder.objects.all().order_by('-created_at')[:20]
    else:
        qs = CustomOrder.objects.filter(status=status_filter).order_by('-created_at')[:20]

    kb = types.InlineKeyboardMarkup(row_width=1)

    if not qs:
        kb.add(types.InlineKeyboardButton('← Назад', callback_data='back_admin_menu'))
        try:
            bot.edit_message_text('📭 Заказов нет.', chat_id=uid,
                                  message_id=call.message.message_id,
                                  parse_mode='HTML', reply_markup=kb)
        except Exception:
            bot.send_message(uid, '📭 Заказов нет.', reply_markup=kb)
        return

    for o in qs:
        st  = STATUS_LABELS.get(o.status, o.status)
        src = '🌐' if o.source == 'site' else '📲'
        lbl = f'{src} #{o.pk} {o.customer_name} | {TYPE_LABELS.get(o.order_type,"")[:15]} | {st}'
        kb.add(types.InlineKeyboardButton(lbl, callback_data=f'admin_order_{o.pk}'))

    kb.add(types.InlineKeyboardButton('← Назад', callback_data='back_admin_menu'))

    title_map = {
        'all': 'Все заказы', 'new': 'Новые', 'processing': 'В обработке',
        'printing': 'Печатаются', 'done': 'Готовые',
    }
    title = title_map.get(status_filter, status_filter)

    try:
        bot.edit_message_text(
            f'📋 <b>{title}</b> (последние 20):',
            chat_id=uid, message_id=call.message.message_id,
            parse_mode='HTML', reply_markup=kb,
        )
        ss(uid, 'admin_list', msg_id=call.message.message_id)
    except Exception:
        m = bot.send_message(uid, f'📋 <b>{title}</b>:', parse_mode='HTML', reply_markup=kb)
        ss(uid, 'admin_list', msg_id=m.message_id)


def _order_text(o):
    """Формирует текст деталей заказа."""
    color_label = f'Разноцветная (+{MULTICOLOR_EXTRA} MDL)' if o.multicolor else 'Одноцветная'
    price_text  = f'{o.total_price} MDL' if o.total_price else 'Индивидуальный расчёт'
    src_label   = '🌐 Сайт' if o.source == 'site' else '📲 Telegram-бот'
    return (
        f'📋 <b>Заказ #{o.pk}</b>  {STATUS_LABELS.get(o.status, o.status)}\n'
        f'Источник: {src_label}\n\n'
        f'<b>👤 Клиент</b>\n'
        f'Имя: {o.customer_name}\n'
        f'Тел: {o.customer_phone}\n'
        f'Адрес: {o.customer_address}\n\n'
        f'<b>📦 Заказ</b>\n'
        f'Тип: {TYPE_LABELS.get(o.order_type, o.order_type)}\n'
        f'Размер: {SIZE_LABELS.get(o.model_size, o.model_size)}\n'
        f'Покраска: {color_label}\n'
        f'Цена: {price_text}\n'
        f'Пожелания: {o.notes or "—"}\n'
        f'Создан: {o.created_at.strftime("%d.%m.%Y %H:%M")}'
    )

def _order_kb(o):
    """Формирует клавиатуру смены статуса."""
    kb = types.InlineKeyboardMarkup(row_width=2)
    status_buttons = [
        ('🔄 В обработке', 'processing'),
        ('🖨 Печатается',  'printing'),
        ('✅ Готов',        'done'),
        ('📦 Доставлен',   'delivered'),
        ('❌ Отменён',      'cancelled'),
    ]
    for label, st in status_buttons:
        if st != o.status:
            kb.add(types.InlineKeyboardButton(label, callback_data=f'admin_setstatus_{o.pk}_{st}'))
    kb.add(types.InlineKeyboardButton('← К списку', callback_data='admin_orders_all'))
    return kb


def show_admin_order_detail(uid, call, order_id):
    try:
        o = CustomOrder.objects.get(pk=order_id)
    except CustomOrder.DoesNotExist:
        bot.answer_callback_query(call.id, '❌ Заказ не найден', show_alert=True)
        return

    text = _order_text(o)
    kb   = _order_kb(o)

    s = gs(uid)
    # has_file_msg — True если текущее сообщение в чате уже содержит файл/фото (caption-режим)
    has_file_msg = s['data'].get('detail_has_file', False)
    detail_order = s['data'].get('detail_order_id')

    # Если переходим к другому заказу — сбрасываем флаг
    if detail_order != order_id:
        has_file_msg = False

    if has_file_msg:
        # Просто обновляем caption существующего медиа-сообщения
        try:
            bot.edit_message_caption(
                caption=text, chat_id=uid,
                message_id=call.message.message_id,
                parse_mode='HTML', reply_markup=kb,
            )
            ss(uid, 'admin_detail', msg_id=call.message.message_id,
               detail_has_file=True, detail_order_id=order_id)
            return
        except Exception:
            pass

    # Нет файла или первый показ — обычный текст
    if not o.uploaded_file:
        try:
            bot.edit_message_text(text, chat_id=uid, message_id=call.message.message_id,
                                  parse_mode='HTML', reply_markup=kb)
            ss(uid, 'admin_detail', msg_id=call.message.message_id,
               detail_has_file=False, detail_order_id=order_id)
        except Exception:
            m = bot.send_message(uid, text, parse_mode='HTML', reply_markup=kb)
            ss(uid, 'admin_detail', msg_id=m.message_id,
               detail_has_file=False, detail_order_id=order_id)
        return

    # Есть файл — отправляем его с caption (текст + кнопки всё в одном сообщении)
    from django.conf import settings as djsettings
    import os as _os
    fp = _os.path.join(djsettings.MEDIA_ROOT, str(o.uploaded_file))
    fname_lower = str(o.uploaded_file).lower()

    # Сначала удаляем старое сообщение (список/предыдущий заказ) чтобы не плодить их
    try:
        bot.delete_message(uid, call.message.message_id)
    except Exception:
        pass

    try:
        if fname_lower.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            with open(fp, 'rb') as f:
                m = bot.send_photo(uid, f, caption=text, parse_mode='HTML', reply_markup=kb)
        else:
            with open(fp, 'rb') as f:
                m = bot.send_document(uid, f, caption=text, parse_mode='HTML', reply_markup=kb)
        ss(uid, 'admin_detail', msg_id=m.message_id,
           detail_has_file=True, detail_order_id=order_id)
    except Exception as e:
        m = bot.send_message(uid, text + f'\n\n⚠️ Файл недоступен: {e}',
                             parse_mode='HTML', reply_markup=kb)
        ss(uid, 'admin_detail', msg_id=m.message_id,
           detail_has_file=False, detail_order_id=order_id)


def admin_set_status(uid, call, order_id, new_status):
    try:
        o = CustomOrder.objects.get(pk=order_id)
    except CustomOrder.DoesNotExist:
        bot.answer_callback_query(call.id, '❌ Заказ не найден', show_alert=True)
        return

    old_status = o.status
    o.status   = new_status
    o.save()

    st_old = STATUS_LABELS.get(old_status, old_status)
    st_new = STATUS_LABELS.get(new_status, new_status)
    bot.answer_callback_query(call.id, f'✅ {st_old} → {st_new}', show_alert=False)

    # Обновляем детали заказа — если есть файл, edit_message_caption; иначе edit_message_text
    o.refresh_from_db()
    text = _order_text(o)
    kb   = _order_kb(o)

    s = gs(uid)
    has_file_msg = s['data'].get('detail_has_file', False)

    if has_file_msg:
        try:
            bot.edit_message_caption(
                caption=text, chat_id=uid,
                message_id=call.message.message_id,
                parse_mode='HTML', reply_markup=kb,
            )
            return
        except Exception:
            pass
    # Fallback — текстовое редактирование
    try:
        bot.edit_message_text(text, chat_id=uid, message_id=call.message.message_id,
                              parse_mode='HTML', reply_markup=kb)
    except Exception:
        pass


# ── ЗАПУСК ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('🤖 3Dprint MD Bot запущен...')
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
