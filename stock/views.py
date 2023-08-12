from django.shortcuts import render,redirect
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

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        
        return redirect('list')
    
    context = {'form': form, 'title': 'Add Item'}
    return render(request, 'add_items.html', context)