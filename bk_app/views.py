from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.forms import modelformset_factory, inlineformset_factory
from django.utils import timezone

from .forms import *
from .models import *


@login_required(login_url='login')
def home(request):
    total_orders = Order.objects.filter(date_created__day=timezone.now().day).count()
    stock_items = StockItem.objects.all()
    context = {'total_orders': total_orders,
               'stock_items': stock_items}
    if request.method == 'POST':
        stock_item = StockItem.objects.get(id=request.POST['stock_item'])
        stock_list = Stock.objects.filter(item_id=request.POST['stock_item'])
        total_added_items = Stock.objects.filter(item_id=request.POST['stock_item'], status='Add')
        total_removed_items = Stock.objects.filter(item_id=request.POST['stock_item'], status='Remove')
        total_added = 0.0
        for add_item in total_added_items:
            total_added += add_item.quantity
        total_removed = 0.0
        for removed_item in total_removed_items:
            total_removed += removed_item.quantity
        price_spent = 0.0
        unit = 'KG'
        for st_item in stock_list:
            price_spent += st_item.price
            unit = st_item.unit
        context = {'stock_item': stock_item,
                   'stock_list': stock_list,
                   'total_added': total_added,
                   'total_taken': total_removed,
                   'price_spent': price_spent,
                   'unit': unit}
        return render(request, 'bk_app/view_stock.html', context)
    return render(request, 'bk_app/home.html', context)


@login_required(login_url='login')
def stock(request):
    stocks = Stock.objects.all()
    stock_items = StockItem.objects.all()
    context = {'stocks': stocks,
               'stock_items': stock_items}
    return render(request, 'bk_app/stock.html', context)


@login_required(login_url='login')
def add_stock_item(request):
    crr_user = User.objects.get(username=request.user)
    if request.method == 'POST':
        stock_item_form = StockItemForm(request.POST)
        if stock_item_form.is_valid():
            obj = stock_item_form.save(commit=False)
            obj.add_by = crr_user
            obj.save()
    stock_item_form = StockItemForm()
    context = {'stock_item_form': stock_item_form, }
    return render(request, 'bk_app/add_stock_item.html', context)


@login_required(login_url='login')
def add_stock(request):
    crr_user = User.objects.get(username=request.user)
    if request.method == 'POST':
        stock_form = StockForm(request.POST)
        if stock_form.is_valid():
            obj = stock_form.save(commit=False)
            obj.add_by = crr_user
            obj.save()
    stock_form = StockForm()
    context = {'stock_form': stock_form, }
    return render(request, 'bk_app/add_stock.html', context)


@login_required(login_url='login')
def menu(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    context = {'categories': categories,
               'menu_items': menu_items}
    return render(request, 'bk_app/menu.html', context)


@login_required(login_url='login')
def add_category(request):
    crr_user = User.objects.get(username=request.user)
    if request.method == 'POST':
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            obj = cat_form.save(commit=False)
            obj.add_by = crr_user
            obj.save()
    cat_form = CategoryForm()
    context = {'cat_form': cat_form, }
    return render(request, 'bk_app/add_category.html', context)


@login_required(login_url='login')
def add_menu_item(request):
    crr_user = User.objects.get(username=request.user)
    if request.method == 'POST':
        menu_item_form = MenuItemForm(request.POST)
        if menu_item_form.is_valid():
            obj = menu_item_form.save(commit=False)
            obj.add_by = crr_user
            obj.save()
    menu_item_form = MenuItemForm()
    context = {'menu_item_form': menu_item_form, }
    return render(request, 'bk_app/add_menu_item.html', context)


@login_required(login_url='login')
def deals(request):
    all_deals = Deal.objects.all()
    context = {'deals': all_deals}
    return render(request, 'bk_app/deals.html', context)


@login_required(login_url='login')
def add_deal(request):
    crr_user = User.objects.get(username=request.user)
    if request.method == 'POST':
        deal_form = DealForm(request.POST)
        if deal_form.is_valid():
            obj = deal_form.save(commit=False)
            obj.add_by = crr_user
            obj.save()
    deal_form = DealForm()
    context = {'deal_form': deal_form, }
    return render(request, 'bk_app/add_deal.html', context)


@login_required(login_url='login')
def view_deal(request, pk):
    deal = Deal.objects.get(id=pk)
    deal_items = deal.dealitem_set.all()
    context = {'deal': deal,
               'deal_items': deal_items}
    return render(request, 'bk_app/view_deal.html', context)


@login_required(login_url='login')
def add_deal_item(request, pk):
    deal = Deal.objects.get(id=pk)
    deal_item_formset = inlineformset_factory(Deal, DealItem, exclude=['deal'], extra=1)
    # deal_item_formset = modelformset_factory(DealItem, exclude=['deal'])
    if request.method == 'POST':
        # formset = deal_item_formset(request.POST, queryset=DealItem.objects.filter(deal_id=pk))
        formset = deal_item_formset(request.POST, instance=deal)
        if formset.is_valid():
            formset.save()
            # instances = formset.save(commit=False)
            # for instance in instances:
            #     instance.deal_id = deal.id
            #     instance.save()
    # formset = deal_item_formset(queryset=DealItem.objects.filter(deal_id=pk))
    formset = deal_item_formset(instance=deal)
    context = {'formset': formset,
               'd_id': pk}
    return render(request, 'bk_app/add_deal_item.html', context)


@login_required(login_url='login')
def orders(request):
    all_orders = Order.objects.all()
    current_orders = Order.objects.filter(date_created__day=timezone.now().day).count()
    # print(current_orders)
    context = {'orders': all_orders}
    return render(request, 'bk_app/orders.html', context)


@login_required(login_url='login')
def add_order(request):
    crr_user = User.objects.get(username=request.user)
    menu_items = MenuItem.objects.all()
    all_deals = Deal.objects.all()
    total_available_deals = all_deals.count()
    total_available_items = menu_items.count()
    order = Order()
    order_no = Order.objects.filter(date_created__day=timezone.now().day).count() + 1
    order_form = OrderForm(instance=order, initial={'no': order_no})
    order_item_inline_form = inlineformset_factory(Order, OrderItem, exclude=('order',), extra=total_available_deals,
                                                   can_delete=False)
    order_menu_item_inline_form = inlineformset_factory(Order, OrderMenuItem, exclude=('order',),
                                                        extra=int(total_available_items * 0.5),
                                                        can_delete=False)
    order_item_forms = order_item_inline_form()
    menu_item_forms = order_menu_item_inline_form()
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        order_item_forms = order_item_inline_form(request.POST, request.FILES)
        menu_item_forms = order_menu_item_inline_form(request.POST, request.FILES)
        if order_form.is_valid():
            created_order = order_form.save(commit=False)
            order_item_forms = order_item_inline_form(request.POST, request.FILES, instance=created_order)
            menu_item_forms = order_menu_item_inline_form(request.POST, request.FILES, instance=created_order)
            if order_item_forms.is_valid() and menu_item_forms.is_valid():
                created_order.save()
                order_item_forms.save()
                menu_item_forms.save()
                new_order = Order.objects.get(id=created_order.id)
                od_items = new_order.orderitem_set.all()
                mi_items = new_order.ordermenuitem_set.all()
                total_price = 0.0
                for d_item in od_items:
                    total_price += d_item.item.price * d_item.quantity
                for m_item in mi_items:
                    total_price += m_item.item.price * m_item.quantity
                charges = total_price
                # add discount
                if new_order.discount > 0:
                    m_discount = new_order.discount / 100
                    total_discount = total_price * m_discount
                    total_price -= total_discount
                new_order.charges = charges
                new_order.bill = total_price
                new_order.add_by = crr_user
                new_order.save()
                return redirect('view_order', pk=new_order.id)
    context = {'order_form': order_form,
               'order_item_form': order_item_forms,
               'menu_item_form': menu_item_forms,
               'menu_items': menu_items,
               'deals': all_deals}
    return render(request, 'bk_app/add_order.html', context)


@login_required(login_url='login')
def view_order(request, pk):
    order = Order.objects.get(id=pk)
    order_items = order.orderitem_set.all()
    menu_items = order.ordermenuitem_set.all()
    context = {'order': order,
               'order_items': order_items,
               'menu_items': menu_items, }
    return render(request, 'bk_app/view_order.html', context)


def do_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'bk_app/login.html')


@login_required(login_url='login')
def do_logout(request):
    logout(request)
    return redirect('home')
