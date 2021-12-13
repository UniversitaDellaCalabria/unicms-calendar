from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from cms.contexts.models import WebPath, WebSite

from cms.api.exceptions import LoggedPermissionDenied
from cms.api.serializers import UniCMSFormSerializer
from cms.api.views.generics import UniCMSCachedRetrieveUpdateDestroyAPIView, UniCMSListCreateAPIView
from cms.api.views.logs import ObjectLogEntriesList

from ... forms import CalendarContextForm
from ... models import CalendarContext
from ... serializers import CalendarContextSerializer


class CalendarContextList(UniCMSListCreateAPIView):
    """
    """
    description = ""
    search_fields = ['calendar__name',]
    serializer_class = CalendarContextSerializer

    def get_queryset(self):
        """
        """
        site_id = self.kwargs.get('site_id')
        webpath_id = self.kwargs.get('webpath_id')
        if site_id and webpath_id:
            site = get_object_or_404(WebSite, pk=site_id, is_active=True)
            if not site.is_managed_by(self.request.user):
                raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                             resource=site)
            webpath = get_object_or_404(WebPath,
                                        pk=webpath_id,
                                        site=site)
            return CalendarContext.objects.filter(webpath=webpath)
        return CalendarContext.objects.none() # pragma: no cover

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # get webpath
            webpath = serializer.validated_data.get('webpath')
            # check permissions on webpath
            perms = webpath.is_publicable_by(user=request.user)
            if not perms:
                raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                             resource=request.method)
            return super().post(request, *args, **kwargs)


class CalendarContextView(UniCMSCachedRetrieveUpdateDestroyAPIView):
    """
    """
    description = ""
    permission_classes = [IsAdminUser]
    serializer_class = CalendarContextSerializer

    def get_queryset(self):
        """
        """
        site_id = self.kwargs['site_id']
        site = get_object_or_404(WebSite, pk=site_id, is_active=True)
        if not site.is_managed_by(self.request.user):
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=site)
        webpath_id = self.kwargs['webpath_id']
        pk = self.kwargs['pk']
        contexts = CalendarContext.objects\
                                  .select_related('webpath')\
                                  .filter(pk=pk,
                                          webpath__pk=webpath_id,
                                          webpath__site__pk=site_id)
        return contexts

    def patch(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item: raise Http404
        webpath = item.webpath
        perms = webpath.is_publicable_by(user=request.user)
        if not perms:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        serializer = self.get_serializer(instance=item,
                                         data=request.data,
                                         partial=True)
        if serializer.is_valid(raise_exception=True):
            new_webpath = serializer.validated_data.get('webpath')
            if new_webpath and new_webpath != item.webpath:
                # check permissions and locks on webpath
                webpath_perms = new_webpath.is_publicable_by(user=request.user)
                if not webpath_perms:
                    raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                                 resource=request.method)
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item: raise Http404
        webpath = item.webpath
        perms = webpath.is_publicable_by(user=request.user)
        if not perms:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        serializer = self.get_serializer(instance=item,
                                         data=request.data,
                                         partial=True)
        if serializer.is_valid(raise_exception=True):
            new_webpath = serializer.validated_data.get('webpath')
            if new_webpath and new_webpath != item.webpath:
                # check permissions and locks on webpath
                webpath_perms = new_webpath.is_publicable_by(user=request.user)
                if not webpath_perms:
                    raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                                 resource=request.method)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        item = self.get_queryset().first()
        if not item: raise Http404
        webpath = item.webpath
        perms = webpath.is_publicable_by(user=request.user)
        if not perms:
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=request.method)
        return super().delete(request, *args, **kwargs)


class CalendarContextFormView(APIView):

    def get(self, *args, **kwargs):
        form = CalendarContextForm(site_id=kwargs.get('site_id'),
                                   webpath_id=kwargs.get('webpath_id'))
        form_fields = UniCMSFormSerializer.serialize(form)
        return Response(form_fields)


class CalendarContextGenericFormView(APIView):

    def get(self, *args, **kwargs):
        form = CalendarContextForm(site_id=kwargs.get('site_id'))
        form_fields = UniCMSFormSerializer.serialize(form)
        return Response(form_fields)


class CalendarContextLogsSchema(AutoSchema):
    def get_operation_id(self, path, method):# pragma: no cover
        return 'lisCalendarContextLogs'


class CalendarContextLogsView(ObjectLogEntriesList):

    schema = CalendarContextLogsSchema()

    def get_queryset(self, **kwargs):
        """
        """
        site_id = self.kwargs['site_id']
        site = get_object_or_404(WebSite, pk=site_id, is_active=True)
        if not site.is_managed_by(self.request.user):
            raise LoggedPermissionDenied(classname=self.__class__.__name__,
                                         resource=site)
        webpath_id = self.kwargs['webpath_id']
        object_id = self.kwargs['pk']
        item = get_object_or_404(CalendarContext.objects.select_related('webpath'),
                                 pk=object_id,
                                 webpath__pk=webpath_id,
                                 webpath__site__pk=site_id)
        content_type_id = ContentType.objects.get_for_model(item).pk
        return super().get_queryset(object_id, content_type_id)
