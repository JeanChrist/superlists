from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from .models import Item, List
from django.core.exceptions import ValidationError
# Create your views here.


def home_page(request):
    return render(request, 'home.html')
    # return HttpResponse('<html><title>To-Do lists</title></html>')


def view_list(request, pk):
    list_obj = List.objects.get(pk=pk)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_obj)
        return redirect(list_obj.get_absolute_url())
    # items = Item.objects.filter(list=list_obj)
    return render(request, 'list.html', {'list': list_obj})


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
    return redirect(list_.get_absolute_url())
