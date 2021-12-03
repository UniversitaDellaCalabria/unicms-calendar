from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cms.api.utils import check_user_permission_on_object
from cms.contexts.models import WebPath
from cms.contexts.models_abstract import AbstractLockable
from cms.contexts.utils import sanitize_path
from cms.publications.models import Publication
from cms.templates.models import (ActivableModel,
                                  CreatedModifiedBy,
                                  SectionAbstractModel,
                                  SortableModel,
                                  TimeStampedModel)

from taggit.managers import TaggableManager


class Calendar(ActivableModel, TimeStampedModel, CreatedModifiedBy,
               AbstractLockable):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=2048,
                                   blank=True,
                                   default='')

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Calendars")

    def serialize(self):
        return {'name': self.name,
                'slug': self.slug,
                'description': self.description,
                # 'events': (
                # {'content': event.publication.serialize(),
                # 'date_start': event.date_start,
                # 'date_end': event.date_end,
                # 'tags': (i.name for i in event.tags.all())} for event in self.calendarevent_set.all()),
                'published_in': (f'{i.webpath.site}{i.webpath.fullpath}'
                                 for i in self.calendarcontext_set.all())}

    def translate_as(self, lang=settings.LANGUAGE):
        i18n = CalendarLocalization.objects.filter(calendar=self,
                                                   language=lang,
                                                   is_active=True)\
                                           .first()
        if i18n:
            self.name = i18n.name
            self.description = i18n.description

    def get_events(self):
        events = CalendarEvent.objects.filter(calendar=self,
                                              is_active=True,
                                              event__is_active=True)
        return events

    def get_future_events(self):
        now = timezone.localtime()
        events = self.get_events().filter(models.Q(event__date_start__gte=now) |
                                          models.Q(event__date_end__gte=now))
        return events

    def __str__(self):
        return self.name


class CalendarLocalization(ActivableModel,
                           TimeStampedModel, SortableModel,
                           CreatedModifiedBy):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    language = models.CharField(choices=settings.LANGUAGES,
                                max_length=12,
                                default='en')
    name = models.CharField(max_length=256,
                            blank=True,
                            default='')
    description = models.TextField(max_length=2048,
                                   blank=True,
                                   default='')

    class Meta:
        verbose_name_plural = _("Calendar Localization")

    def is_lockable_by(self, user):
        item = self.calendar
        permission = check_user_permission_on_object(user=user, obj=item)
        return permission['granted']

    def __str__(self):
        return '{} {}'.format(self.calendar, self.language)


class Event(ActivableModel, TimeStampedModel,
            SortableModel, CreatedModifiedBy):
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL,
                                    blank=True, null=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = _("Calendar events")
        ordering = ['date_start']

    def translate_as(self, lang=settings.LANGUAGE):
        self.publication.translate_as(lang)

    # def is_lockable_by(self, user):
        # item = self.calendar
        # permission = check_user_permission_on_object(user=user, obj=item)
        # return permission['granted']

    def __str__(self):
        return '{}'.format(self.publication)


class CalendarEvent(ActivableModel, TimeStampedModel,
                    SortableModel, CreatedModifiedBy):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Calendar event relations")
        ordering = ['calendar__pk', 'event__date_start']
        unique_together = ('event', 'calendar')

    def translate_as(self, lang=settings.LANGUAGE):
        self.calendar.translate_as(lang)
        self.event.translate_as(lang)

    def __str__(self):
        return '[{}] {}'.format(self.calendar, self.event)


class CalendarContext(TimeStampedModel, ActivableModel,
                      SectionAbstractModel, SortableModel,
                      CreatedModifiedBy):
    calendar = models.ForeignKey(Calendar, on_delete=models.PROTECT)
    webpath = models.ForeignKey(WebPath, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Calendar Contexts")
        ordering = ['webpath__fullpath', 'order']

    def translate_as(self, lang=settings.LANGUAGE):
        self.calendar.translate_as(lang=lang)

    @property
    def path_prefix(self):
        return settings.CMS_CALENDAR_VIEW_PREFIX_PATH

    @property
    def url(self):
        url = f'{self.webpath.get_full_path()}{self.path_prefix}/{self.calendar.slug}/'
        return sanitize_path(url)

    # def get_url_list(self, category_name=None):
        # list_prefix = getattr(settings, 'CMS_CALENDAR_LIST_PREFIX_PATH',
        # CMS_CALENDAR_LIST_PREFIX_PATH)
        # url = sanitize_path(f'{self.webpath.get_full_path()}/{list_prefix}')
        # if category_name:
        # url += f'/?category_name={category_name}'
        # return sanitize_path(url)

    # def get_absolute_url(self):
        # return self.url

    # @property
    # def name(self):
        # return self.calendar.name

    # def translate_as(self, *args, **kwargs):
        # self.calendar.translate_as(*args, **kwargs)

    # def serialize(self):
        # result = self.publication.serialize()
        # result['path'] = self.url
        # return result

    # def is_lockable_by(self, user):
        # return self.webpath.is_publicable_by(user)

    def __str__(self):
        return '{} {}'.format(self.calendar, self.webpath)
