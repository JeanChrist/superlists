from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from .models import Item
# Create your views here.


def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


def home_page(request):
    # post_text = request.POST.get('item_text', '')
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    return render(request, 'home.html', {'items': Item.objects.all()})
    # return HttpResponse('<html><title>To-Do lists</title></html>')
