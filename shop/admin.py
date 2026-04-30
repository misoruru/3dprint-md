from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Product, ProductImage, Order, PortfolioPhoto, CustomOrder, ProductAttachment

admin.site.site_header = '3Dprint MD — Панель управления'
admin.site.site_title  = '3Dprint MD'
admin.site.index_title = 'Добро пожаловать!'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'order', 'product_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<b>{}</b> шт.', count)
    product_count.short_description = 'Продуктов'



class ProductAttachmentInline(admin.TabularInline):
    model  = ProductAttachment
    extra  = 1
    fields = ['attach_type', 'title', 'file', 'url', 'preview_link']
    readonly_fields = ['preview_link']

    def preview_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📎 Скачать</a>', obj.file.url)
        if obj.url:
            return format_html('<a href="{}" target="_blank">🔗 Открыть</a>', obj.url)
        return '—'
    preview_link.short_description = 'Открыть'

class ProductImageInline(admin.TabularInline):
    model    = ProductImage
    extra    = 3
    fields   = ['image', 'order', 'allow_selection', 'preview']
    readonly_fields = ['preview']
    ordering = ['order']

    def preview(self, obj):
        if obj.image:
            badge = ''
            if obj.allow_selection:
                badge = '<br><span style="background:#22c55e;color:#000;font-size:0.7rem;padding:1px 6px;border-radius:4px;font-weight:700">✓ Выбор</span>'
            return format_html(
                '<img src="{}" style="height:80px;border-radius:6px;object-fit:cover;">{}',
                obj.image.url, badge
            )
        return '—'
    preview.short_description = 'Превью'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ['main_image_col', 'name', 'slug', 'price', 'genre', 'featured', 'photo_count', 'created_at']
    list_filter    = ['genre', 'featured']
    search_fields  = ['name', 'slug', 'description']
    list_editable  = ['featured', 'price']
    ordering       = ['-featured', 'name']
    inlines        = [ProductImageInline, ProductAttachmentInline]
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Основное',        {'fields': ('slug', 'name', 'genre', 'featured')}),
        ('Характеристики',  {'fields': ('price', 'material', 'size', 'print_time', 'colors')}),
        ('Описание',        {'fields': ('description',)}),
        ('📝 Заметки для себя', {'fields': ('admin_notes',), 'classes': ('collapse',), 'description': 'Видны только в админке. Сюда можно писать ссылки, комментарии, напоминания.'}),
    )

    def main_image_col(self, obj):
        img = obj.main_image()
        if img:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:6px;">',
                img.url
            )
        return format_html('<span style="color:#666;font-size:0.8rem;">нет фото</span>')
    main_image_col.short_description = 'Фото'

    def photo_count(self, obj):
        count = obj.images.count()
        color = '#22c55e' if count > 0 else '#ef4444'
        return format_html('<span style="color:{};font-weight:bold;">{} шт.</span>', color, count)
    photo_count.short_description = 'Фото'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ['id', 'customer_name', 'customer_phone', 'product', 'total_price', 'status', 'status_badge', 'created_at']
    list_filter     = ['status', 'created_at']
    search_fields   = ['customer_name', 'customer_phone']
    list_editable   = ['status']
    readonly_fields = ['created_at', 'chosen_photo_preview']

    fieldsets = (
        ('Клиент',  {'fields': ('customer_name', 'customer_phone', 'customer_address')}),
        ('Заказ',   {'fields': ('product', 'color', 'fill', 'notes', 'total_price', 'chosen_photo_preview')}),
        ('Статус',  {'fields': ('status', 'created_at')}),
    )

    def chosen_photo_preview(self, obj):
        if obj.chosen_photo:
            return format_html(
                '<img src="{}" style="height:120px;border-radius:8px;object-fit:cover;"><br>'
                '<a href="{}" target="_blank" style="font-size:0.8rem;">🔗 Открыть фото</a>',
                obj.chosen_photo, obj.chosen_photo
            )
        return format_html('<span style="color:#888;">Покупатель не выбрал фото</span>')
    chosen_photo_preview.short_description = '📸 Выбранное фото'

    def status_badge(self, obj):
        colors = {
            'new':        ('#00f0ff', '#000'),
            'processing': ('#ffa500', '#000'),
            'printing':   ('#a855f7', '#fff'),
            'done':       ('#22c55e', '#000'),
            'delivered':  ('#16a34a', '#fff'),
            'cancelled':  ('#ef4444', '#fff'),
        }
        bg, fg = colors.get(obj.status, ('#888', '#fff'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:5px;font-size:0.78rem;font-weight:700">{}</span>',
            bg, fg, obj.get_status_display()
        )
    status_badge.short_description = '🏷'


@admin.register(PortfolioPhoto)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    list_display  = ['preview_col', 'title', 'order', 'is_visible', 'created_at']
    list_editable = ['order', 'is_visible']
    list_filter   = ['is_visible']
    ordering      = ['order', '-created_at']

    def preview_col(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;width:80px;object-fit:cover;border-radius:6px;">',
                obj.image.url
            )
        return '—'
    preview_col.short_description = 'Превью'


@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display    = ['id', 'customer_name', 'customer_phone', 'order_type', 'model_size', 'multicolor', 'total_price', 'source', 'status', 'status_badge', 'file_link', 'created_at']
    list_filter     = ['status', 'order_type', 'multicolor', 'source', 'created_at']
    search_fields   = ['customer_name', 'customer_phone']
    list_editable   = ['status']
    readonly_fields = ['created_at', 'file_link']

    fieldsets = (
        ('Клиент',  {'fields': ('customer_name', 'customer_phone', 'customer_address')}),
        ('Заказ',   {'fields': ('order_type', 'model_size', 'multicolor', 'notes', 'uploaded_file', 'file_link')}),
        ('Цена',    {'fields': ('total_price',)}),
        ('Статус',  {'fields': ('status', 'source', 'created_at')}),
    )

    def file_link(self, obj):
        if obj.uploaded_file:
            return format_html('<a href="{}" target="_blank">📎 Скачать файл</a>', obj.uploaded_file.url)
        return '—'
    file_link.short_description = 'Файл'

    def chosen_photo_preview(self, obj):
        if obj.chosen_photo:
            return format_html(
                '<img src="{}" style="height:120px;border-radius:8px;object-fit:cover;"><br>'
                '<a href="{}" target="_blank" style="font-size:0.8rem;">🔗 Открыть фото</a>',
                obj.chosen_photo, obj.chosen_photo
            )
        return format_html('<span style="color:#888;">Покупатель не выбрал фото</span>')
    chosen_photo_preview.short_description = '📸 Выбранное фото'

    def status_badge(self, obj):
        colors = {
            'new':        ('#00f0ff', '#000'),
            'processing': ('#ffa500', '#000'),
            'printing':   ('#a855f7', '#fff'),
            'done':       ('#22c55e', '#000'),
            'delivered':  ('#16a34a', '#fff'),
            'cancelled':  ('#ef4444', '#fff'),
        }
        bg, fg = colors.get(obj.status, ('#888', '#fff'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:5px;font-size:0.78rem;font-weight:700">{}</span>',
            bg, fg, obj.get_status_display()
        )
    status_badge.short_description = '🏷'
