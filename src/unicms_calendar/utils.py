import logging



logger = logging.getLogger(__name__)


def calendar_context_base_filter():
    calcontxt_filter = {'calendar__is_active': True,
                        'is_active': True}
    return calcontxt_filter
