from django.db import models
from django.core.exceptions import ValidationError

class MenuNames(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu_name = models.ForeignKey(MenuNames, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=70, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sorting_order = models.IntegerField(null=True, blank=True)

    def clean(self):
        if self.parent is not None and self.menu_name != self.parent.menu_name:
            raise ValidationError('Parent item must have the same menu_name')

    def __str__(self):
        return self.label