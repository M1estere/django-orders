# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Order, Item
from .forms import OrderForm, ItemForm

def order_list(request):
    query = request.GET.get('q')
    orders = Order.objects.all()

    if query:
        status_key = Order.get_status_value(query.lower())
        if status_key:
            orders = orders.filter(
                Q(table_number__icontains=query) | 
                Q(status__icontains=status_key)
            )
        else:
            orders = orders.filter(table_number__icontains=query)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
    })

def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()

            items_selected = order_form.cleaned_data['items']
            for item in items_selected:
                order.items.add(item)
            
            order.update_total_price()
            return redirect('order_list')
    else:
        order_form = OrderForm()
    
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
    })

def order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        
        if order_form.is_valid():
            order_form.save()
            return redirect('order_list')
    else:
        order_form = OrderForm(instance=order)

    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'order': order,
    })

def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')

def revenue_report(request):
    paid_orders = Order.objects.filter(status='paid')
    
    total_revenue = sum(order.total_price for order in paid_orders)

    return render(request, 'orders/revenue_report.html', {
        'total_revenue': total_revenue,
        'paid_orders': paid_orders,
    })

def item_list(request):
    items = Item.objects.all()
    return render(request, 'orders/item_list.html', {
        'items': items,
    })

def item_create(request, item_id=None):
    if item_id:
        item = get_object_or_404(Item, id=item_id)
        item_form = ItemForm(request.POST or None, instance=item)
    else:
        item_form = ItemForm(request.POST or None)
    
    if request.method == 'POST' and item_form.is_valid():
        item = item_form.save()

        orders = Order.objects.filter(items=item)
        for order in orders:
            order.total_price = sum(item.price for item in order.items.all())
            order.save()

        return redirect('item_list')
    
    return render(request, 'orders/item_form.html', {
        'item_form': item_form,
    })

def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('item_list')
