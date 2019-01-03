from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', kwargs={'pk': self.pk})
        # return f'/lists/{self.pk}/'


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('list', 'text')

    # def validate_unique(self):
    #     super().validate_unique()