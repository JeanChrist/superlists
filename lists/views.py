from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from .models import Item, List
# Create your views here.


def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


def home_page(request):
    return render(request, 'home.html')
    # return HttpResponse('<html><title>To-Do lists</title></html>')


def view_list(request, pk):
    list_obj = List.objects.get(pk=pk)
    # items = Item.objects.filter(list=list_obj)
    return render(request, 'list.html', {'list': list_obj})


def create_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(list_.get_absolute_url())


def create_item(request, list_id):
    list_ = List.objects.get(pk=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(list_.get_absolute_url())
