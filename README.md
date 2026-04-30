# 3Dprint MD — Django

## Быстрый старт

```bash
# 1. Установи зависимости
pip install -r requirements.txt

# 2. Применить миграции (уже применены, но если база пустая)
python manage.py migrate

# 3. Заполнить продукты (уже выполнено)
python manage.py seed_products

# 4. Создать суперпользователя (уже создан: admin / admin123)
python manage.py createsuperuser

# 5. Запустить сервер
python manage.py runserver
```

## Доступ

| URL | Описание |
|-----|----------|
| http://localhost:8000/ | Главная страница |
| http://localhost:8000/catalog/ | Каталог |
| http://localhost:8000/admin/ | Django Admin |
| http://localhost:8000/api/products | JSON API продуктов |

## Логин в Admin

- Логин: **admin**
- Пароль: **admin123**

> Поменяй пароль после первого входа!

## В Admin можно

- Добавлять / редактировать / удалять продукты
- Смотреть заказы и менять их статус (Новый → Печатается → Готов → Доставлен)
- Загружать фото для продуктов
