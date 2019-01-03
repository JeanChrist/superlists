from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm, EMPTY_ITEM_ERROR, ExistingListItemForm

# Create your views here.


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})
    # return HttpResponse('<html><title>To-Do lists</title></html>')


def view_list(request, pk):
    list_obj = List.objects.get(pk=pk)
    form = ExistingListItemForm(list_obj)
    if request.method == 'POST':
        form = ExistingListItemForm(list_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_obj)

    return render(request, 'list.html', {'list': list_obj, "form": form})


def create_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():

        list_obj = List.objects.create()
        form.save(list_obj)
        return redirect(list_obj)
    return render(request, 'home.html', {"form": form})
