from django.shortcuts import render
from .forms import StockCreateForm
from .models import Stock

def home(request):
    title = 'Hello to my page'
    form = StockCreateForm()
    context = {'title': title, 'form': form}
    return render(request, 'home.html', context)

def list_items(request):
    title = 'List'
    qs = Stock.objects.all()
    context = {'title': title, 'qs': qs}
    return render(request, 'list.html', context)