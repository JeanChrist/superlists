from django.db import models


class List(models.Model):
    def get_absolute_url(self):
        return f'/lists/{self.pk}/'


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
