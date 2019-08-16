from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Menu, Item, Ingredient
from .forms import MenuForm, ItemForm


def menu_list(request):
    """View that list all menus that are available."""
    all_menus = Menu.objects.filter(
        expiration_date__gte=timezone.now()
        ).prefetch_related('items')
    return render(request, 'menu/list_all_current_menus.html', {'menus': all_menus})


def menu_detail(request, pk):
    """View that list the detail of a menu."""
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def create_new_menu(request):
    """View that lets a registered user create a new menu."""
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_form.html', {'form': form})


def edit_menu(request, pk):
    """View that lets a registered user edit a menu."""
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)

    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=menu.pk)

    return render(request, 'menu/menu_form.html', {'form': form,})


def item_list(request):
    """View that list all items alphabetically with a limit of 10 per page."""
    all_items = Item.objects.all()
    paginator = Paginator(all_items, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    return render(request, 'menu/item_list.html', {'items': items})


def item_detail(request, pk):
    """View that list the detailed ingredients of the selected item."""
    try: 
        item = Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/item_detail.html', {'item': item})


def create_new_item(request):
    """View that lets the current user(chef) create new items."""
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.chef = request.user
            item.save()
            form.save_m2m()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'menu/item_form.html', {'form': form})


def edit_item(request, pk):
    """View that lets the related chef edit the item."""
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(instance=item)

    if request.method == "POST":
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk=item.pk)

    return render(request, 'menu/item_form.html', {'form': form,})
