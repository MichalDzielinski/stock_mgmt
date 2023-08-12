from django.contrib import admin
from django.urls import path
from stock import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.list_items, name='list'),
    path('add_items/', views.add_items, name='add_items'),
    path('admin/', admin.site.urls),
]
