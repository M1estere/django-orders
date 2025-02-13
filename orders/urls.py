# orders/urls.py

from django.urls import path, include
from .views import order_list, order_create, order_edit, order_delete, item_create, item_list, revenue_report, item_delete
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('edit/<int:order_id>/', order_edit, name='order_edit'),
    path('delete/<int:order_id>/', order_delete, name='order_delete'),
    path('revenue/', revenue_report, name='revenue_report'),

    path('items/', item_list, name='item_list'),
    path('items/create/', item_create, name='item_create'),
    path('items/create/<int:item_id>/', item_create, name='item_create'),
    path('items/delete/<int:item_id>/', item_delete, name='item_delete'),

    path('api/', include(router.urls)),
]
