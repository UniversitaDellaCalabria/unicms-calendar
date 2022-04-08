import logging

from django import template
from django.conf import settings


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def editorial_board_event_edit(item):
    if not hasattr(settings, 'EDITORIAL_BOARD_EVENT_EDIT_URL'): return '#'
    return settings.EDITORIAL_BOARD_EVENT_EDIT_URL.format(event=item.pk)
