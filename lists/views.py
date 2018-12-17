from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.http import HttpResponse
# Create your views here.


def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


def home_page(request):
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
    # return HttpResponse('<html><title>To-Do lists</title></html>')
