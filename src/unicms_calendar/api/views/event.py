import logging

from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from cms.api.exceptions import LoggedPermissionDenied
from cms.api.serializers import UniCMSFormSerializer
from cms.api.utils import check_user_permission_on_object
from cms.api.views.generics import UniCMSCachedRetrieveUpdateDestroyAPIView, UniCMSListCreateAPIView, UniCMSListSelectOptionsAPIView
from cms.api.views.logs import ObjectLogEntriesList

from .. permissions import EventGetCreatePermissions
from ... forms import *
from ... models import Event
from ... serializers import *


logger = logging.getLogger(__name__)


class EventList(UniCMSListCreateAPIView):
    """
    """
    description = ""
    ordering_fields = ['publication__name','publication__title',
                       'is_active','order','id']
    search_fields = ['publication__title']
    permission_classes = [EventGetCreatePermissions]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventView(UniCMSCachedRetrieveUpdateDestroyAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        """
        event_id = self.kwargs['pk']
        events = Event.objects.filter(pk=event_id)
        return events

    def patch(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item:
            raise Http404
        permission = check_user_permission_on_object(request.user,
                                                     item)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item:
            raise Http404
        permission = check_user_permission_on_object(request.user,
                                                     item)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item:
            raise Http404
        permission = check_user_permission_on_object(request.user,
                                                     item, 'delete')
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().delete(request, *args, **kwargs)


class EventFormView(APIView):

    def get(self, *args, **kwargs):
        form = EventForm()
        form_fields = UniCMSFormSerializer.serialize(form)
        return Response(form_fields)


class EventLogsSchema(AutoSchema):
    def get_operation_id(self, path, method):  # pragma: no cover
        return 'listEventLogs'


class EventLogsView(ObjectLogEntriesList):

    schema = EventLogsSchema()

    def get_queryset(self, **kwargs):
        """
        """
        object_id = self.kwargs['pk']
        item = get_object_or_404(Event, pk=object_id)
        content_type_id = ContentType.objects.get_for_model(item).pk
        return super().get_queryset(object_id, content_type_id)


class EventOptionListSchema(AutoSchema):
    def get_operation_id(self, path, method):  # pragma: no cover
        return 'listEventSelectOptions'


class EventOptionList(UniCMSListSelectOptionsAPIView):
    """
    """
    description = ""
    search_fields = ['publication__name', 'publication__title']
    serializer_class = EventSelectOptionsSerializer
    queryset = Event.objects.all()
    schema = EventOptionListSchema()


class EventOptionView(generics.RetrieveAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = EventSelectOptionsSerializer

    def get_queryset(self):
        """
        """
        event_id = self.kwargs['pk']
        event = Event.objects.filter(pk=event_id)
        return event
