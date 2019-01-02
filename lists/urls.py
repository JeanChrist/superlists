from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.view_list, name='view_list'),
    path('create', views.create_list, name='lists_create'),
]
