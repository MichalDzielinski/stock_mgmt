from django.shortcuts import render,redirect
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm
from .models import Stock

def home(request):
    title = 'Hello to my page'
    form = StockCreateForm()
    context = {'title': title, 'form': form}
    return render(request, 'home.html', context)

def list_items(request):
    header = 'List'
    form = StockSearchForm(request.POST or None)
    qs = Stock.objects.all()
    context = {'header': header, 'qs': qs, 'form': form}

    if request.method == 'POST':
            qs = Stock.objects.filter( category__icontains = form['category'].value(), 
                                         item_name__icontains=form['item_name'].value())
    context = {'header': header, 'qs': qs, 'form': form}
    
    return render(request, 'list.html', context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        
        return redirect('list')
    
    context = {'form': form, 'title': 'Add Item'}
    return render(request, 'add_items.html', context)

def update_item(request, pk):
    qs = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=qs)
    if request.method == 'POST':
          form = StockUpdateForm(request.POST, instance=qs)
          if form.is_valid():
               form.save()
               return redirect('list')
    context = {'form': form}
    return render(request, 'add_items.html', context)

def delete_item(request, pk):
     qs = Stock.objects.get(id=pk)
     if request.method == 'POST':
          qs.delete()
          return redirect('list')
     return render(request, 'delete_item.html')




