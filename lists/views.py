from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from .models import Item
# Create your views here.


def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


def home_page(request):
    return render(request, 'home.html')
    # return HttpResponse('<html><title>To-Do lists</title></html>')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def create_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
