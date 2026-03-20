# 3Dprint MD — Структура проекта

## 📁 Файловая структура

```
3dprint-md/
├── index.html          ← Главная страница
├── catalog.html        ← Каталог моделей
│
├── css/
│   ├── shared.css      ← Общие стили (nav, footer, modal, form, variables)
│   ├── index.css       ← Стили только главной страницы
│   └── catalog.css     ← Стили только каталога
│
├── js/
│   ├── products.js     ← База данных товаров (общая)
│   ├── modals.js       ← Логика модальных окон заказа (общая)
│   ├── starry-bg.js    ← Анимация звёздного фона (общая)
│   ├── index.js        ← Логика главной страницы
│   └── catalog.js      ← Логика каталога
│
├── images/             ← Фотографии фигурок
│   ├── hero-image.png      (главная — изображение принтера/фигурки)
│   ├── dragon-warrior.png
│   ├── cyber-cat.png
│   ├── space-explorer.png
│   ├── mystic-wizard.png
│   ├── robo-buddy.png
│   └── skull-guardian.png
│
└── components/
    ├── header.html     ← HTML шапки (для справки / при переходе на шаблонизатор)
    └── footer.html     ← HTML подвала (для справки)
```

---

## 🚀 Деплой на Vercel (рекомендуется)

### 1. Через GitHub
```bash
# Инициализировать Git в папке проекта
cd 3dprint-md
git init
git add .
git commit -m "Initial commit"

# Создать репозиторий на github.com, затем:
git remote add origin https://github.com/ВАШ_ЮЗЕР/3dprint-md.git
git push -u origin main
```
Потом зайти на [vercel.com](https://vercel.com) → **Add New Project** → выбрать репозиторий → **Deploy**.  
Vercel автоматически определит статический сайт. Домен подключается в **Settings → Domains**.

### 2. Через Vercel CLI
```bash
npm install -g vercel
cd 3dprint-md
vercel
```

---

## 🐍 Деплой через Django (для будущей backend-логики)

### Установка
```bash
pip install django
django-admin startproject backend
cd backend
python manage.py startapp shop
```

### Структура Django
```
backend/
├── backend/
│   └── settings.py     ← добавить STATICFILES_DIRS
├── shop/
│   ├── views.py        ← рендер index.html, catalog.html
│   ├── urls.py
│   └── models.py       ← модель Order (заказы из формы)
├── templates/          ← скопировать index.html, catalog.html сюда
└── static/             ← скопировать css/, js/, images/ сюда
```

### settings.py
```python
TEMPLATES = [{'DIRS': [BASE_DIR / 'templates'], ...}]
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'
```

### views.py
```python
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def catalog(request):
    return render(request, 'catalog.html')
```

### urls.py
```python
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index),
    path('catalog/', views.catalog),
]
```

В HTML заменить пути к статике:
```html
<!-- Было -->
<link rel="stylesheet" href="css/shared.css">
<!-- Стало (Django) -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/shared.css' %}">
```

---

## ✏️ Как добавить новый товар

1. Открыть `js/products.js`
2. Добавить новый объект в `productDatabase`:
```js
'New Product': {
    name: 'Название на русском',
    price: 399,
    material: 'Фотополимерная смола',
    size: '12-15 см',
    time: '8-12 часов',
    colors: 'Серый, Многоцветный',
    description: 'Описание товара.',
    images: ['🦄', '✨', '🌟', '💫']  // потом заменить на реальные фото
},
```
3. Добавить карточку в `index.html` (секция `#popular`) и/или в `catalog.html`

---

## 🖼️ Как подключить реальные фото вместо эмодзи

Сейчас вместо фото используются эмодзи. Когда будут реальные фото:

1. Положить фото в папку `images/`
2. В `js/products.js` в поле `images` поменять эмодзи на пути:
```js
images: ['images/dragon-warrior.png', 'images/dragon-warrior-2.png']
```
3. В `js/index.js` и `js/catalog.js` поменять логику отображения:
```js
// Вместо: element.textContent = image
// Написать:
if (image.startsWith('images/')) {
    element.innerHTML = `<img src="${image}" alt="${name}" style="width:100%;height:100%;object-fit:contain;">`;
} else {
    element.textContent = image;
}
```

---

## 📦 Подключение домена на Vercel

1. Купить домен (например на [namecheap.com](https://namecheap.com) или [molddata.md](https://www.molddata.md))
2. В Vercel: **Settings → Domains → Add Domain** → ввести домен
3. В панели регистратора домена добавить DNS-записи которые покажет Vercel:
   - Тип `A` → IP Vercel
   - Тип `CNAME` → `cname.vercel-dns.com`
4. Подождать 10-30 минут — сайт заработает на домене
