from django.contrib import admin
from .models import MenuItem, MenuNames

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ('label', 'menu_name', 'url', 'named_url', 'parent', 'sorting_order')

@admin.register(MenuNames)
class MenuNamesAdmin(admin.ModelAdmin):
	list_display = ('name',)