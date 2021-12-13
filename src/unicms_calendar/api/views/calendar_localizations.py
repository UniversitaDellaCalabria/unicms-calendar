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
from cms.api.views.generics import *
from cms.api.views.logs import ObjectLogEntriesList

from ... forms import CalendarLocalizationForm
from ... models import *
from ... serializers import *


class CalendarLocalizationList(UniCMSListCreateAPIView):
    """
    """
    description = ""
    search_fields = ['language', 'name']
    permission_classes = [IsAdminUser]
    serializer_class = CalendarLocalizationSerializer

    def get_queryset(self):
        """
        """
        calendar_id = self.kwargs.get('calendar_id')
        if calendar_id:
            return CalendarLocalization.objects.filter(calendar__pk=calendar_id)
        return CalendarLocalization.objects.none() # pragma: no cover

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


class CalendarLocalizationView(UniCMSCachedRetrieveUpdateDestroyAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = CalendarLocalizationSerializer

    def get_queryset(self):
        """
        """
        calendar_id = self.kwargs['calendar_id']
        item_id = self.kwargs['pk']
        items = CalendarLocalization.objects\
                                        .select_related('calendar')\
                                        .filter(pk=item_id,
                                                calendar__pk=calendar_id)
        return items

    def patch(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item: raise Http404
        calendar = item.calendar
        # check permissions on calendar
        permission = check_user_permission_on_object(request.user,
                                                     calendar)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item: raise Http404
        calendar = item.calendar
        # check permissions on calendar
        permission = check_user_permission_on_object(request.user,
                                                     calendar)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item: raise Http404
        calendar = item.calendar
        # check permissions on calendar
        permission = check_user_permission_on_object(request.user,
                                                     calendar)
        if not permission['granted']:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().delete(request, *args, **kwargs)


class CalendarLocalizationFormView(APIView):

    def get(self, *args, **kwargs):
        form = CalendarLocalizationForm(calendar_id=kwargs.get('calendar_id'))
        form_fields = UniCMSFormSerializer.serialize(form)
        return Response(form_fields)


class CalendarLocalizationLogsSchema(AutoSchema):
    def get_operation_id(self, path, method):# pragma: no cover
        return 'listCalendarLocalizationLogs'


class CalendarLocalizationLogsView(ObjectLogEntriesList):

    schema = CalendarLocalizationLogsSchema()

    def get_queryset(self, **kwargs):
        """
        """
        calendar_id = self.kwargs['calendar_id']
        object_id = self.kwargs['pk']
        item = get_object_or_404(CalendarLocalization.objects.select_related('calendar'),
                                 pk=object_id,
                                 calendar__pk=calendar_id)
        content_type_id = ContentType.objects.get_for_model(item).pk
        return super().get_queryset(object_id, content_type_id)
