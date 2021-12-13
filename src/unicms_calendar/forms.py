from django.forms import ModelForm
from django.urls import reverse

from cms.api.settings import FORM_SOURCE_LABEL
from cms.contexts.models import WebPath

from . models import *


class CalendarForm(ModelForm):

    class Meta:
        model = Calendar
        fields = ['name', 'slug', 'description', 'is_active']


class EventForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setattr(self.fields['publication'],
                FORM_SOURCE_LABEL,
                # only images
                reverse('unicms_api:editorial-board-publications-options'))

    class Meta:
        model = Event
        fields = ['publication', 'date_start', 'date_end',
                  'order', 'is_active', ]


class CalendarEventForm(ModelForm):

    def __init__(self, *args, **kwargs):
        calendar_id = kwargs.pop('calendar_id', None)
        super().__init__(*args, **kwargs)
        if calendar_id:
            self.fields['calendar'].queryset = Calendar.objects.filter(pk=calendar_id)
        setattr(self.fields['event'],
                FORM_SOURCE_LABEL,
                reverse('unicms_calendar:event-options'))

    class Meta:
        model = CalendarEvent
        fields = ['calendar', 'event', 'order', 'is_active']


class CalendarContextForm(ModelForm):

    def __init__(self, *args, **kwargs):
        site_id = kwargs.pop('site_id', None)
        webpath_id = kwargs.pop('webpath_id', None)
        super().__init__(*args, **kwargs)
        if site_id:
            if webpath_id:
                self.fields['webpath'].queryset = WebPath.objects.filter(pk=webpath_id,
                                                                         site__pk=site_id)
            else:
                self.fields['webpath'].queryset = WebPath.objects.filter(site__pk=site_id)
            setattr(self.fields['webpath'],
                    FORM_SOURCE_LABEL,
                    reverse('unicms_api:webpath-options',
                            kwargs={'site_id': site_id}))
        setattr(self.fields['calendar'],
                FORM_SOURCE_LABEL,
                reverse('unicms_calendar:calendar-options'))

    class Meta:
        model = CalendarContext
        fields = ['webpath', 'calendar',
                  'order', 'is_active']


class CalendarLocalizationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        calendar_id = kwargs.pop('calendar_id', None)
        super().__init__(*args, **kwargs)
        if calendar_id:
            self.fields['calendar'].queryset = Calendar.objects.filter(pk=calendar_id)

    class Meta:
        model = CalendarLocalization
        fields = ['calendar', 'language', 'name',
                  'description', 'order', 'is_active']
