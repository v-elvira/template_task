from collections import defaultdict
from django import template
from django.urls import reverse, resolve
from treemenu.models import MenuItem

from django.utils.html import format_html

register = template.Library()

# Recursively generate html for item and its children
def draw_item(item, menu_dict, top_parent, active_parents):
    is_active = item == top_parent

    menu_html = ['<li{}>'.format(' class="has_children"' if menu_dict[item] else ''),]
    if is_active:
        menu_html.append('<span class="active">')
    if item.url:
        menu_html.append('<a href="{}">{}</a>'.format(item.url, item.label))
    elif item.named_url:
        menu_html.append('<a href="{}">{}</a>'.format(reverse(item.named_url), item.label))
    else:
        menu_html.append('{}'.format(item.label))
    if is_active:
        menu_html.append('</span>')

    if is_active and menu_dict[item]:
        menu_html.append('<ul>')
        current_parent =  None if not len(active_parents) else active_parents.pop()
        for child_item in menu_dict[item]:
            menu_html.extend(draw_item(child_item, menu_dict, current_parent, active_parents))
        menu_html.append('</ul>')
    menu_html.append('</li>')
    return menu_html

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    # Get the current URL and view name
    current_url = context['request'].path
    current_view_name = resolve(current_url).view_name

    # Retrieve the menu items for the specified menu name
    menu_items = MenuItem.objects.filter(menu_name__name=menu_name).order_by('sorting_order')
    if not menu_items:
        return format_html('')

    active_item = None

    # Create a dictionary of menu items and their child items
    menu_dict = defaultdict(list)
    for item in menu_items:
        menu_dict[item.parent].append(item)

        # Check if item is currently active
        item_url = item.url
        if len(item_url) > 0 and item_url[0] != '/':
            item_url = '/' + item_url
        if item_url == current_url or item.named_url == current_view_name:
            active_item = item

    # Create a stack of active item parents
    active_parents = []
    while active_item is not None:
        active_parents.append(active_item)
        active_item = active_item.parent

    # Recursively generate HTML code for the menu
    menu_html = ['<ul>',]
    top_parent = None if not len(active_parents) else active_parents.pop()
    for item in menu_dict[None]:
        menu_html.extend(draw_item(item, menu_dict, top_parent, active_parents))
    menu_html.append('</ul>')
    return format_html(''.join(menu_html))
