from django.contrib import admin

from . models import CalendarContext, CalendarEvent, CalendarLocalization


class CalendarEventInline(admin.StackedInline):
    model = CalendarEvent
    extra = 0
    sortable_field_name = "order"
    classes = ['collapse']
    raw_id_fields = ('event',)


class CalendarLocalizationInline(admin.TabularInline):
    model = CalendarLocalization
    extra = 0
    sortable_field_name = "order"
    classes = ['collapse']


class CalendarContextInline(admin.StackedInline):
    model = CalendarContext
    extra = 0
    classes = ['collapse']
    raw_id_fields = ('webpath',)
    readonly_fields = ('created_by', 'modified_by')
