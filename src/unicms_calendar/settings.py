CMS_CALENDAR_VIEW_PREFIX_PATH = 'contents/calendars/view'
CMS_CALENDAR_LIST_PREFIX_PATH = 'contents/calendars/list'

CMS_CALENDAR_URL_LIST_REGEXP = f'^(?P<webpath>[\/a-zA-Z0-9\.\-\_]*)({CMS_CALENDAR_LIST_PREFIX_PATH})(/)?$'
CMS_CALENDAR_URL_VIEW_REGEXP = f'^(?P<webpath>[\/a-zA-Z0-9\.\-\_]*)({CMS_CALENDAR_VIEW_PREFIX_PATH})/(?P<slug>[a-zA-Z0-9\-\_]*)(/)?$'
CMS_CALENDAR_EVENT_URL_VIEW_REGEXP = f'^(?P<webpath>[\/a-zA-Z0-9\.\-\_]*)({CMS_CALENDAR_VIEW_PREFIX_PATH})/(?P<slug>[a-zA-Z0-9\-\_]*)/(?P<event>[a-zA-Z0-9\-\_]*)(/)?$'

CMS_CALENDAR_HANDLERS_PATHS = [
    CMS_CALENDAR_URL_LIST_REGEXP,
    CMS_CALENDAR_URL_VIEW_REGEXP,

    CMS_CALENDAR_EVENT_URL_VIEW_REGEXP
]

CMS_CALENDAR_APP_REGEXP_URLPATHS = {
    'unicms_calendar.handlers.CalendarListHandler': CMS_CALENDAR_URL_LIST_REGEXP,
    'unicms_calendar.handlers.CalendarViewHandler': CMS_CALENDAR_URL_VIEW_REGEXP,
    'unicms_calendar.handlers.CalendarEventViewHandler': CMS_CALENDAR_EVENT_URL_VIEW_REGEXP,
}

CMS_CALENDAR_HOOKS = {
    'Event': {
        'PRESAVE': [],
        'POSTSAVE': ['unicms_calendar.hooks.event_se_insert',],
                     # 'cms.contexts.hooks.used_by'],
        'PREDELETE': ['cms.search.hooks.searchengine_entry_remove',],
        'POSTDELETE': []
    },
    'CalendarEvent': {
        'PRESAVE': [],
        'POSTSAVE': ['unicms_calendar.hooks.calendar_event_se_insert',],
                     # 'cms.contexts.hooks.used_by'],
        'PREDELETE': ['cms.search.hooks.searchengine_entry_remove',],
        'POSTDELETE': []
    },
}

CMS_CALENDAR_MONGO_MAP = {
    'unicms_calendar.Event': 'unicms_calendar.search.event_to_entry'
}

# SITEMAP PRIORITY
SITEMAP_CALENDAR_PRIORITY = 0.6
