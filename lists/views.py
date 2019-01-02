from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm

# Create your views here.


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})
    # return HttpResponse('<html><title>To-Do lists</title></html>')


def view_list(request, pk):
    list_obj = List.objects.get(pk=pk)
    error = None
    if request.method == 'POST':

        try:
            item = Item(text=request.POST['item_text'], list=list_obj)
            item.full_clean()
            item.save()
            return redirect(list_obj)
        except ValidationError:
            error = "You can't have an empty list item"
        # Item.objects.create(text=request.POST['item_text'], list=list_obj)
        # return redirect(list_obj.get_absolute_url())
    # items = Item.objects.filter(list=list_obj)
    return render(request, 'list.html', {'list': list_obj, 'error': error})


def create_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"

        return render(request, 'home.html', {'error': error})
    return redirect(list_)
