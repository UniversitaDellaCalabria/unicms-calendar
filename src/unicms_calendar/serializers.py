from django.urls import reverse

from cms.publications.serializers import PublicationSerializer

from rest_framework import serializers

from . models import *
from . settings import CMS_CALENDAR_VIEW_PREFIX_PATH

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class CalendarContextSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        calendar = CalendarSerializer(instance.calendar)
        data['calendar'] = calendar.data
        data['path'] = instance.url
        return data

    class Meta:
        model = CalendarContext
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class EventSerializer(serializers.ModelSerializer):

    # tags = TagListSerializerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        publication = PublicationSerializer(instance.publication)
        data['publication_data'] = publication.data
        return data

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class CalendarEventSerializer(serializers.ModelSerializer):

    # tags = TagListSerializerField()

    def to_representation(self, instance):

        data = super().to_representation(instance)
        event = EventSerializer(instance.event)
        data['event'] = event.data
        calendar = CalendarSerializer(instance.calendar)
        data['calendar'] = calendar.data

        webpath_id = self.context.get('webpath_id', None)
        if webpath_id:
            data['calendar_url'] = f'{CMS_CALENDAR_VIEW_PREFIX_PATH}/{instance.calendar.slug}/'
            data['event_url'] = f'{CMS_CALENDAR_VIEW_PREFIX_PATH}/{instance.calendar.slug}/{instance.event.pk}/'

        return data

    class Meta:
        model = CalendarEvent
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class CalendarSelectOptionsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['value'] = instance.pk
        data['text'] = instance.name
        return data

    class Meta:
        model = Calendar
        fields = ()


class EventSelectOptionsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['value'] = instance.pk
        data['text'] = instance.name
        return data

    class Meta:
        model = Event
        fields = ()
