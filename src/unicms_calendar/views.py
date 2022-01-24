from django.conf import settings
from django.contrib.sitemaps import GenericSitemap

from cms.contexts.views import _get_site_from_host

from . import settings as app_settings
from . models import CalendarContext


SITEMAP_CALENDAR_PRIORITY = getattr(settings, 'SITEMAP_CALENDAR_PRIORITY',
                                    app_settings.SITEMAP_CALENDAR_PRIORITY)


def unicms_calendar_sitemap(request):
    website = _get_site_from_host(request)
    protocol =  request.scheme

    calendar_map = {
        'queryset': CalendarContext.objects.filter(webpath__site=website,
                                                   webpath__is_active=True,
                                                   is_active=True),
        'date_field': 'modified',
    }

    sitemap_dict = {
        'calendars': GenericSitemap(calendar_map,
                                    priority=SITEMAP_CALENDAR_PRIORITY,
                                    protocol=protocol),
        }

    return sitemap_dict
