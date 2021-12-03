import logging

from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from cms.contexts.decorators import detect_language

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from cms.api.exceptions import LoggedPermissionDenied
from cms.api.serializers import UniCMSFormSerializer
from cms.api.utils import check_user_permission_on_object
from cms.api.views.generics import UniCMSCachedRetrieveUpdateDestroyAPIView, UniCMSListCreateAPIView, UniCMSListSelectOptionsAPIView, UniCmsApiPagination
from cms.api.views.logs import ObjectLogEntriesList

from .. permissions import CalendarGetCreatePermissions
from ... forms import *
from ... models import CalendarContext, CalendarEvent
from ... serializers import *
from ... utils import calendar_context_base_filter


logger = logging.getLogger(__name__)


@method_decorator(detect_language, name='dispatch')
class ApiContextCalendars(generics.ListAPIView):
    """
    """
    description = 'ApiContextCalendars'
    pagination_class = UniCmsApiPagination
    serializer_class = CalendarContextSerializer

    def get_queryset(self):
        """
        """
        webpath_id = self.kwargs['webpath_id']
        query_params = calendar_context_base_filter()
        query_params.update({'webpath__pk': webpath_id})
        calcontx = CalendarContext.objects.filter(**query_params)

        # i18n
        lang = getattr(self.request, 'LANGUAGE_CODE', None)
        if lang:
            for ctx in calcontx:
                ctx.translate_as(lang)
        return calcontx


@method_decorator(detect_language, name='dispatch')
class ApiContextCalendar(generics.RetrieveAPIView):
    """
    """
    description = 'ApiContextCalendar'
    serializer_class = CalendarContextSerializer

    def get_queryset(self):
        webpath_id = self.kwargs['webpath_id']
        calendar_id = self.kwargs['pk']
        query_params = calendar_context_base_filter()
        query_params.update({'webpath__pk': webpath_id,
                             'calendar__pk': calendar_id})

        calcontx = CalendarContext.objects.filter(**query_params)
        return calcontx


@method_decorator(detect_language, name='dispatch')
class ApiContextCalendarsEvents(generics.ListAPIView):
    """
    """
    description = 'ApiContextCalendarsEvents'
    pagination_class = UniCmsApiPagination
    serializer_class = CalendarEventSerializer

    def get_serializer_context(self):
        context = super(ApiContextCalendarsEvents, self).get_serializer_context()
        context.update({"webpath_id": self.kwargs['webpath_id']})
        return context

    def get_queryset(self):
        """
        """
        webpath_id = self.kwargs['webpath_id']
        query_params = calendar_context_base_filter()
        query_params.update({'webpath__pk': webpath_id})
        calendars = CalendarContext.objects.filter(**query_params)

        # i18n
        lang = getattr(self.request, 'LANGUAGE_CODE', None)
        events = []

        for cal_ctx in calendars:
            cal_events = cal_ctx.calendar.get_future_events()
            for event in cal_events:
                if lang:
                    event.translate_as(lang)
                events.append(event)
        return events


@method_decorator(detect_language, name='dispatch')
class ApiContextCalendarEvents(generics.ListAPIView):
    """
    """
    description = 'ApiContextCalendarEvents'
    pagination_class = UniCmsApiPagination
    serializer_class = CalendarEventSerializer

    def get_serializer_context(self):
        context = super(ApiContextCalendarEvents, self).get_serializer_context()
        context.update({"webpath_id": self.kwargs['webpath_id']})
        return context

    def get_queryset(self):
        """
        """
        webpath_id = self.kwargs['webpath_id']
        calendar_id = self.kwargs['calendar_id']
        query_params = calendar_context_base_filter()
        query_params.update({'webpath__pk': webpath_id,
                             'calendar__pk': calendar_id})
        calcontx = get_object_or_404(CalendarContext, **query_params)
        events = calcontx.calendar.get_future_events()

        # i18n
        lang = getattr(self.request, 'LANGUAGE_CODE', None)
        if lang:
            [event.translate_as(lang) for event in events]

        return events


@method_decorator(detect_language, name='dispatch')
class ApiContextCalendarEvent(generics.RetrieveAPIView):
    """
    """
    description = 'ApiContextCalendarEvent'
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        """
        """
        webpath_id = self.kwargs['webpath_id']
        calendar_id = self.kwargs['calendar_id']
        event_id = self.kwargs['pk']
        query_params = calendar_context_base_filter()
        query_params.update({'webpath__pk': webpath_id,
                             'calendar__pk': calendar_id})
        calcontx = get_object_or_404(CalendarContext, **query_params)
        event = CalendarEvent.objects.filter(calendar=calcontx.calendar,
                                             event__pk=event_id,
                                             is_active=True)

        return event


class CalendarList(UniCMSListCreateAPIView):
    """
    """
    description = ""
    search_fields = ['name', 'description']
    permission_classes = [CalendarGetCreatePermissions]
    serializer_class = CalendarSerializer
    queryset = Calendar.objects.all()


class CalendarView(UniCMSCachedRetrieveUpdateDestroyAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = CalendarSerializer

    def get_queryset(self):
        """
        """
        calendar_id = self.kwargs['pk']
        calendars = Calendar.objects.filter(pk=calendar_id)
        return calendars

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


class CalendarFormView(APIView):

    def get(self, *args, **kwargs):
        form = CalendarForm()
        form_fields = UniCMSFormSerializer.serialize(form)
        return Response(form_fields)


class CalendarLogsSchema(AutoSchema):
    def get_operation_id(self, path, method):  # pragma: no cover
        return 'listCalendarLogs'


class CalendarLogsView(ObjectLogEntriesList):

    schema = CalendarLogsSchema()

    def get_queryset(self, **kwargs):
        """
        """
        object_id = self.kwargs['pk']
        item = get_object_or_404(Calendar, pk=object_id)
        content_type_id = ContentType.objects.get_for_model(item).pk
        return super().get_queryset(object_id, content_type_id)


class CalendarOptionListSchema(AutoSchema):
    def get_operation_id(self, path, method):  # pragma: no cover
        return 'listCalendarSelectOptions'


class CalendarOptionList(UniCMSListSelectOptionsAPIView):
    """
    """
    description = ""
    search_fields = ['name']
    serializer_class = CalendarSelectOptionsSerializer
    queryset = Calendar.objects.all()
    schema = CalendarOptionListSchema()


class CalendarOptionView(generics.RetrieveAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = CalendarSelectOptionsSerializer

    def get_queryset(self):
        """
        """
        calendar_id = self.kwargs['pk']
        calendar = Calendar.objects.filter(pk=calendar_id)
        return calendar
