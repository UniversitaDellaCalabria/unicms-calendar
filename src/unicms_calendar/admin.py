
from django.contrib import admin

from cms.contexts.admin import AbstractCreatedModifiedBy

from . admin_inlines import *
from . models import *


@admin.register(Calendar)
class CalendarAdmin(AbstractCreatedModifiedBy):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('created', 'modified')
    inlines = (CalendarEventInline,
               CalendarLocalizationInline,
               CalendarContextInline)
    readonly_fields = ('created_by', 'modified_by')


@admin.register(Event)
class EventAdmin(AbstractCreatedModifiedBy):
    list_display = ('publication', 'date_start',
                    'date_end', 'is_active')
    search_fields = ('publication__name', 'publication__title',)
    list_filter = ('created', 'modified', 'date_start', 'date_end')
    readonly_fields = ('created_by', 'modified_by')
    raw_id_fields = ('publication',)
