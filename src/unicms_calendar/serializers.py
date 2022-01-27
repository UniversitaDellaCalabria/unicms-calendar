from django.urls import reverse
from django.utils import timezone

from cms.api.serializers import UniCMSContentTypeClass, UniCMSCreateUpdateSerializer
from cms.contexts.serializers import WebPathSerializer
from cms.publications.serializers import PublicationSerializer, WebPathForeignKey

from rest_framework import serializers

from . models import *
from . settings import CMS_CALENDAR_VIEW_PREFIX_PATH

class CalendarSerializer(UniCMSCreateUpdateSerializer,
                         UniCMSContentTypeClass):
    class Meta:
        model = Calendar
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class EventSerializer(UniCMSCreateUpdateSerializer,
                      UniCMSContentTypeClass):

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


class CalendarEventSerializer(UniCMSCreateUpdateSerializer,
                              UniCMSContentTypeClass):

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


class CalendarSelectOptionsSerializer(UniCMSCreateUpdateSerializer,
                                      UniCMSContentTypeClass):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['value'] = instance.pk
        data['text'] = instance.name
        return data

    class Meta:
        model = Calendar
        fields = ()


class EventSelectOptionsSerializer(UniCMSCreateUpdateSerializer,
                                   UniCMSContentTypeClass):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['value'] = instance.pk
        data['text'] = f'{instance.publication.name} [{timezone.localtime(instance.date_start)} - {timezone.localtime(instance.date_end)}]'
        return data

    class Meta:
        model = Event
        fields = ()


class CalendarContextSerializer(UniCMSCreateUpdateSerializer,
                                UniCMSContentTypeClass):
    webpath = WebPathForeignKey()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        calendar = CalendarSerializer(instance.calendar)
        data['calendar'] = calendar.data
        webpath = WebPathSerializer(instance.webpath)
        data['webpath'] = webpath.data
        data['path'] = instance.url
        return data

    class Meta:
        model = CalendarContext
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class CalendarLocalizationSerializer(UniCMSCreateUpdateSerializer,
                                         UniCMSContentTypeClass):
    class Meta:
        model = CalendarLocalization
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')
