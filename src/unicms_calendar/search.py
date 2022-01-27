from django.conf import settings
from django.utils import timezone

from cms.search.models import SearchEntry


DEFAULT_LANGUAGE = dict(settings.LANGUAGES)[settings.LANGUAGE].lower()


def event_to_entry(event_object, exclude_calevent=None):
    app_label, model = event_object._meta.label_lower.split('.')
    contexts = event_object.get_event_contexts(exclude_calevent=exclude_calevent)
    if not contexts: return
    first_context = contexts.first()
    urls = set([f'//{i.webpath.site.domain}{i.url}{event_object.pk}' for i in contexts])
    sites = set([f'{i.webpath.site.domain}' for i in contexts])
    data = {
        "title": event_object.publication.title,
        "heading": event_object.publication.subheading,
        "content_type": event_object._meta.label,
        "image": event_object.publication.image_url(),
        "content_id": event_object.pk,
        "content": event_object.publication.content,
        "sites": list(sites),
        "urls": list(urls),
        # "categories": [i.name for i in pub_object.categories.all()],
        "categories": ['Evento'],
        # "tags": [i for i in pub_object.tags.values_list('name', flat=1)],
        "tags": [],
        "translations": [{'language': i[1].lower(),
                          'title': i[0].title,
                          'subheading': i[0].subheading,
                          'content': i[0].content
                         }
                         for i in event_object.publication.available_in_languages],
        "indexed": timezone.localtime(),
        "published": event_object.created,
        "viewed": 0,
        "language": DEFAULT_LANGUAGE,
        "day": event_object.date_start.day,
        "month": event_object.date_start.month,
        "year": event_object.date_start.year
    }
    search_entry = SearchEntry(**data)
    return search_entry.dict()
