from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template import Template, Context
from django.utils.translation import gettext_lazy as _

from cms.contexts.handlers import BaseContentHandler
from cms.contexts.utils import contextualize_template, sanitize_path
from cms.pages.models import Page

from . models import *
from . settings import *
from . utils import calendar_context_base_filter


class CalendarViewHandler(BaseContentHandler):
    template = "unicms_calendar.html"

    def __init__(self, **kwargs):
        super(CalendarViewHandler, self).__init__(**kwargs)
        self.match_dict = self.match.groupdict()
        query = calendar_context_base_filter()
        query.update(dict(webpath__site=self.website,
                          webpath__fullpath=self.match_dict.get(
                              'webpath', '/'),
                          calendar__slug=self.match_dict.get('slug', '')
                          )
                     )
        self.cal_context = CalendarContext.objects.filter(**query).first()
        if not hasattr(self.cal_context, 'webpath'):  # pragma: no cover
            raise Http404('Unknown WebPath')

        self.page = Page.objects.filter(is_active=True,
                                        webpath=self.cal_context.webpath)\
                                .first()
        self.webpath = self.cal_context.webpath

    def as_view(self):
        if not self.cal_context:
            return Http404()

        # i18n
        lang = getattr(self.request, 'LANGUAGE_CODE', None)
        if lang:
            self.cal_context.translate_as(lang=lang)

        data = {'request': self.request,
                'lang': lang,
                'webpath': self.webpath,
                'website': self.website,
                'page': self.page,
                'path': self.match_dict.get('webpath', '/'),
                'calendar_context': self.cal_context,
                'handler': self}

        ext_template_sources = contextualize_template(self.template,
                                                      self.page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)

    @property
    def parent_path_prefix(self):
        return getattr(settings, 'CMS_CALENDAR_LIST_PREFIX_PATH',
                       CMS_CALENDAR_LIST_PREFIX_PATH)

    @property
    def parent_url(self):
        url = f'{self.webpath.get_full_path()}/{self.parent_path_prefix}/'
        return sanitize_path(url)

    @property
    def breadcrumbs(self):
        leaf = (self.cal_context.url,
                getattr(self.cal_context.calendar, 'name'))
        parent = (self.parent_url, _('Calendars'))
        return (parent, leaf)


class CalendarListHandler(BaseContentHandler):
    template = "unicms_calendars.html"

    @property
    def breadcrumbs(self):
        path = self.path
        leaf = (path, _('Calendars'))
        return (leaf,)

    def as_view(self):
        match_dict = self.match.groupdict()
        page = Page.objects.filter(is_active=True,
                                   webpath__site=self.website,
                                   webpath__fullpath=match_dict.get('webpath', '/')).first()
        if not page:  # pragma: no cover
            raise Http404('Unknown Web Page')
        data = {'request': self.request,
                'webpath': page.webpath,
                'website': self.website,
                'page': page,
                'path': match_dict.get('webpath', '/'),
                'handler': self,
                }

        ext_template_sources = contextualize_template(self.template, page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)


class CalendarEventViewHandler(BaseContentHandler):
    template = "unicms_event.html"

    def __init__(self, **kwargs):
        super(CalendarEventViewHandler, self).__init__(**kwargs)
        self.match_dict = self.match.groupdict()
        query = calendar_context_base_filter()
        query.update(dict(webpath__site=self.website,
                          webpath__fullpath=self.match_dict.get(
                              'webpath', '/'),
                          calendar__slug=self.match_dict.get('slug', ''),
                          )
                     )
        self.cal_context = get_object_or_404(CalendarContext, **query)
        if not hasattr(self.cal_context, 'webpath'):  # pragma: no cover
            raise Http404('Unknown WebPath')

        self.calendar_event = get_object_or_404(CalendarEvent,
                                                calendar=self.cal_context.calendar,
                                                is_active=True,
                                                event__is_active=True,
                                                event__pk=self.match_dict.get('event', ''))
        self.page = Page.objects.filter(is_active=True,
                                        webpath=self.cal_context.webpath)\
            .first()
        self.webpath = self.cal_context.webpath

    def as_view(self):
        # i18n
        lang = getattr(self.request, 'LANGUAGE_CODE', None)
        if lang:
            self.calendar_event.translate_as(lang=lang)

        data = {'request': self.request,
                'webpath': self.webpath,
                'website': self.website,
                'page': self.page,
                'path': self.match_dict.get('webpath', '/'),
                'calendar_context': self.cal_context,
                'event': self.calendar_event.event,
                'handler': self}

        ext_template_sources = contextualize_template(self.template,
                                                      self.page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)

    @property
    def calendars_path_prefix(self):
        return getattr(settings, 'CMS_CALENDAR_LIST_PREFIX_PATH',
                       CMS_CALENDAR_LIST_PREFIX_PATH)

    @property
    def parent_path_prefix(self):
        return getattr(settings, 'CMS_CALENDAR_VIEW_PREFIX_PATH',
                       CMS_CALENDAR_VIEW_PREFIX_PATH)

    @property
    def calendars_url(self):
        url = f'{self.webpath.get_full_path()}/{self.calendars_path_prefix}/'
        return sanitize_path(url)

    @property
    def parent_url(self):
        url = f'{self.webpath.get_full_path()}/{self.parent_path_prefix}/{self.cal_context.calendar.slug}/'
        return sanitize_path(url)

    @property
    def breadcrumbs(self):
        leaf = (self.cal_context.url,
                self.calendar_event.event.publication.title)
        parent = (self.parent_url, self.calendar_event.calendar.name)
        calendars = (self.calendars_url, _('Calendars'))
        return (calendars, parent, leaf)
