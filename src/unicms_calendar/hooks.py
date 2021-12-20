import logging

from django.conf import settings as global_settings
from django.utils import timezone

from cms.search import mongo_collection

from . search import event_to_entry

logger = logging.getLogger(__name__)


MONGO_DB_NAME = getattr(global_settings, 'MONGO_DB_NAME')
MONGO_COLLECTION_NAME = getattr(global_settings, 'MONGO_COLLECTION_NAME')


def event_se_insert(event_object):
    collection = mongo_collection()

    search_entry = event_to_entry(event_object)
    if search_entry:
        search_entry = search_entry
    else:
        return
    # check if it doesn't exists or remove it and recreate
    doc_query = {"content_type": event_object._meta.label,
                 "content_id": search_entry['content_id']}
    doc = collection.find_one(doc_query)
    if doc:
        collection.delete_many(doc_query)
        logger.info(f'{event_object} removed from search engine')

    # now = timezone.localtime()
    # publicable_context = contexts.filter(date_start__lte=now,
                                         # date_end__gt=now)

    # if pub_object.is_publicable:
    # if publicable_context:
        # doc = collection.insert_one(search_entry)
    doc = collection.insert_one(search_entry)
    logger.info(f'{event_object} succesfully indexed in search engine')
