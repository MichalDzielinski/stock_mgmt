from django.contrib import admin
from django.urls import path
from stock import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.list_items, name='list'),
    path('add_items/', views.add_items, name='add_items'),
    path('add_items/<int:pk>/', views.update_item, name='update_item'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('stock_detail/<str:pk>/', views.stock_detail, name='stock_detail'),

    path('admin/', admin.site.urls),
]
