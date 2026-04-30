from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('api/products', views.api_products, name='api_products'),
    path('api/genres', views.api_genres, name='api_genres'),
    path('api/portfolio', views.api_portfolio, name='api_portfolio'),
    path('api/order', views.api_order, name='api_order'),
    path('api/custom-order', views.api_custom_order, name='api_custom_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
