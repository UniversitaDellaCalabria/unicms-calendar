from django.forms import ModelForm
from django.urls import reverse

from cms.api.settings import FORM_SOURCE_LABEL

from . models import Calendar, CalendarEvent, Event


class CalendarForm(ModelForm):

    class Meta:
        model = Calendar
        fields = ['name', 'description', 'is_active']


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
                  'tags', 'order', 'is_active', ]


class CalendarEventForm(ModelForm):

    def __init__(self, *args, **kwargs):
        calendar_id = kwargs.pop('calendar_id', None)
        super().__init__(*args, **kwargs)
        if calendar_id:
            self.fields['calendar'].queryset = Calendar.objects.filter(
                pk=calendar_id)
        setattr(self.fields['event'],
                FORM_SOURCE_LABEL,
                reverse('unicms_calendar:event-options'))

    class Meta:
        model = CalendarEvent
        fields = ['calendar', 'event', 'order', 'is_active']
