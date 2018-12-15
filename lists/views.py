from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.http import HttpResponse
# Create your views here.


def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')