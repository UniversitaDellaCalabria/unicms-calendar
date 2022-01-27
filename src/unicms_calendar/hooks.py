import logging

from django.conf import settings as global_settings
from django.utils import timezone

from cms.search import mongo_collection

from . search import event_to_entry

logger = logging.getLogger(__name__)


MONGO_DB_NAME = getattr(global_settings, 'MONGO_DB_NAME')
MONGO_COLLECTION_NAME = getattr(global_settings, 'MONGO_COLLECTION_NAME')


def event_se_insert(event_object, *args, **kwargs):
    collection = mongo_collection()

    # check if it doesn't exists or remove it and recreate
    doc_query = {"content_type": event_object._meta.label,
                 "content_id": str(event_object.pk)}
    doc = collection.find_one(doc_query)
    if doc:
        collection.delete_many(doc_query)
        logger.info(f'{event_object} removed from search engine')

    if not event_object.is_active: return

    exclude_calendar_event = kwargs.get('exclude_context', None)

    search_entry = event_to_entry(event_object,
                                  exclude_calendar_event=exclude_calendar_event)
    if search_entry:
        search_entry = search_entry
    else:
        return

    doc = collection.insert_one(search_entry)
    logger.info(f'{event_object} succesfully indexed in search engine')


def calendar_event_se_insert(cal_event_object):
    event_object = cal_event_object.event
    event_se_insert(event_object)


def calendar_event_se_delete(cal_event_object, *args, **kwargs):
    event_object = cal_event_object.event
    event_se_insert(pub_object,
                    exclude_calendar_event=cal_event_object.pk,
                    *args, **kwargs)
