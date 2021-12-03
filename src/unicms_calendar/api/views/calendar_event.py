import logging

from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from cms.api.exceptions import LoggedPermissionDenied
from cms.api.serializers import UniCMSFormSerializer
from cms.api.utils import check_user_permission_on_object
from cms.api.views.generics import UniCMSCachedRetrieveUpdateDestroyAPIView, UniCMSListCreateAPIView
from cms.api.views.logs import ObjectLogEntriesList

from ... forms import *
from ... models import CalendarContext, CalendarEvent
from ... serializers import *


logger = logging.getLogger(__name__)


class CalendarEventList(UniCMSListCreateAPIView):
    """
    """
    description = ""
    search_fields = ['event__publication__title']
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        """
        """
        calendar_id = self.kwargs.get('calendar_id')
        if calendar_id:
            return CalendarEvent.objects.filter(calendar__pk=calendar_id)
        return CalendarEvent.objects.none()  # pragma: no cover

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # get calendar
            calendar = serializer.validated_data.get('calendar')
            # check permissions on calendar
            permission = check_user_permission_on_object(request.user,
                                                         calendar)
            if not permission['granted']:
                raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                             resource=request.method)

            return super().post(request, *args, **kwargs)


class CalendarEventView(UniCMSCachedRetrieveUpdateDestroyAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        """
        """
        calendar_id = self.kwargs['calendar_id']
        event_id = self.kwargs['pk']
        calendar_events = CalendarEvent.objects.filter(calendar__pk=calendar_id,
                                                       pk=event_id)
        return calendar_events

    def patch(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item:
            raise Http404
        # get calendar
        item.calendar
        permission = check_user_permission_on_object(request.user,
                                                     item.calendar)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item:
            raise Http404
        # get calendar
        item.calendar
        permission = check_user_permission_on_object(request.user,
                                                     item.calendar)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item:
            raise Http404
        # get calendar
        item.calendar
        permission = check_user_permission_on_object(request.user,
                                                     item.calendar)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().delete(request, *args, **kwargs)


class CalendarEventFormView(APIView):

    def get(self, *args, **kwargs):
        form = CalendarEventForm(calendar_id=kwargs.get('calendar_id'))
        form_fields = UniCMSFormSerializer.serialize(form)
        return Response(form_fields)


class CalendarEventLogsSchema(AutoSchema):
    def get_operation_id(self, path, method):  # pragma: no cover
        return 'listCalendarEventLogs'


class CalendarEventLogsView(ObjectLogEntriesList):

    schema = CalendarEventLogsSchema()

    def get_queryset(self, **kwargs):
        """
        """
        object_id = self.kwargs['pk']
        item = get_object_or_404(CalendarEvent, pk=object_id)
        content_type_id = ContentType.objects.get_for_model(item).pk
        return super().get_queryset(object_id, content_type_id)
