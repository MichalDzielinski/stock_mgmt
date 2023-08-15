import csv
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm
from .models import Stock, StockHistory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    title = 'Hello to my page'
    form = StockCreateForm()
    context = {'title': title, 'form': form}
    return render(request, 'home.html', context)

@login_required
def list_items(request):
    header = 'List'
    form = StockSearchForm(request.POST or None)
    qs = Stock.objects.all()
    context = {'header': header, 'qs': qs, 'form': form}

    if request.method == 'POST':
            qs = Stock.objects.filter( 
                #  category__icontains = form['category'].value(), 
                                         item_name__icontains=form['item_name'].value())
            if form['export_to_CSV'].value() ==True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=List_of_stock.csv'
                writer = csv.writer(response)
                writer.writerow(['CATEGORY','ITEM NAME', 'QUANTITY'])
                instance = qs
                for s in instance:
                      writer.writerow([s.category, s.item_name, s.quantity])
                return response        
    context = {'header': header, 'qs': qs, 'form': form}
    return render(request, 'list.html', context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item successfully created!')

        
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
            messages.success(request, 'Item successfully updated!')

            return redirect('list')
    context = {'form': form}
    return render(request, 'add_items.html', context)

def delete_item(request, pk):
     qs = Stock.objects.get(id=pk)
     if request.method == 'POST':
          qs.delete()
          messages.success(request, 'Item successfully deleted!')
          return redirect('list')
     return render(request, 'delete_item.html')

def stock_detail(request, pk):
     qs = Stock.objects.get(id=pk)
     context = {
          'title': qs.item_name,
          'qs': qs
     }
     return render(request, 'stock_detail.html', context)

def issue_items(request, pk):
    qs = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=qs)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        
        messages.success(request, 'Issued SUCCESSFULLY. ' + str(instance.quantity)+' '+str(instance.item_name)+'s now left in store')
        instance.save()

        return redirect('/stock_detail/'+str(instance.id))
    context = {
         "title": 'Issue '+str(qs.item_name),
         'qs': qs,
         'form': form,
         'username': "Issue by: "+str(request.user)
    }
    return render(request, 'add_items.html', context)

def receive_items(request, pk):
    qs = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=qs)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. "+str(instance.quantity)+' '+str(instance.item_name)+'s now in Store')

        return redirect('/stock_detail/'+str(instance.id))
    
    context = {
         'title': "Receive "+str(qs.item_name),
         'instance': qs,
         'form': form,
         'username': 'Receive by: '+str(request.user)
    }
    return render(request, 'add_items.html', context)

def reorder_level(request, pk):
    qs = Stock.objects.get(id=pk)
    form =  ReorderLevelForm(request.POST or None, instance = qs)
    if form.is_valid():
         instance = form.save(commit=False)
         instance.save()
         messages.success(request, 'Reorder level for '+str(instance.item_name)+" is update to "+str(instance.reorder_level))

         return redirect('list')
    context = {
         'instance': qs,
         'form': form
    }
    return render(request, 'add_items.html', context)

@login_required
def list_history(request):
    header = 'LIST OF ITEMS'
    qs = StockHistory.objects.all()
    context = {
         'header': header,
         'qs': qs
    }
    return render(request, 'list_history.html', context)







