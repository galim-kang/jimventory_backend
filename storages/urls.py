# storages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StorageViewSet, MenuViewSet, StorageCreateView, UpdateStorageView

router = DefaultRouter()
router.register(r'storages', StorageViewSet, basename='storage')
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', StorageCreateView.as_view(), name='storage-create'),
    path('update/<int:pk>/', UpdateStorageView.as_view(), name='storage-update'),
]
