from django.urls import path

from cms.api.urls import eb_prefix

from . api.views import (calendar, calendar_event,
                         event, calendar_contexts,
                         calendar_localizations)


# CMS_PATH_PREFIX = getattr(settings, 'CMS_PATH_PREFIX', '')
_board_base = 'unicms_calendar'

urlpatterns = []

urlpatterns += path('api/calendars/by-context/<int:webpath_id>/', calendar.ApiContextCalendars.as_view(), name='api-context-calendars'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/<int:pk>/', calendar.ApiContextCalendar.as_view(), name='api-context-calendar'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/events/', calendar.ApiContextCalendarsEvents.as_view(), name='api-context-calendars-events'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/<int:calendar_id>/events/', calendar.ApiContextCalendarEvents.as_view(), name='api-context-calendar-events'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/<int:calendar_id>/events/<int:pk>/', calendar.ApiContextCalendarEvent.as_view(), name='api-context-calendar-event'),

# calendars
cal_prefix = f'{eb_prefix}/calendars'
urlpatterns += path(f'{cal_prefix}/', calendar.CalendarList.as_view(), name='calendars'),
urlpatterns += path(f'{cal_prefix}/<int:pk>/', calendar.CalendarView.as_view(), name='calendar'),
urlpatterns += path(f'{cal_prefix}/<int:pk>/logs/', calendar.CalendarLogsView.as_view(), name='calendar-logs'),
urlpatterns += path(f'{cal_prefix}/form/', calendar.CalendarFormView.as_view(), name='calendar-form'),
urlpatterns += path(f'{cal_prefix}/options/', calendar.CalendarOptionList.as_view(), name='calendar-options'),
urlpatterns += path(f'{cal_prefix}/options/<int:pk>/', calendar.CalendarOptionView.as_view(), name='calendar-option'),

# calendar localizations
calo = f'{cal_prefix}/<int:calendar_id>/localizations'
urlpatterns += path(f'{calo}/', calendar_localizations.CalendarLocalizationList.as_view(), name='calendar-localizations'),
urlpatterns += path(f'{calo}/<int:pk>/', calendar_localizations.CalendarLocalizationView.as_view(), name='calendar-localization'),
urlpatterns += path(f'{calo}/<int:pk>/logs/', calendar_localizations.CalendarLocalizationLogsView.as_view(), name='calendar-localization-logs'),
urlpatterns += path(f'{calo}/form/', calendar_localizations.CalendarLocalizationFormView.as_view(), name='calendar-localization-form'),

# events
ev_prefix = f'{eb_prefix}/events'
urlpatterns += path(f'{ev_prefix}/', event.EventList.as_view(), name='events'),
urlpatterns += path(f'{ev_prefix}/<int:pk>/', event.EventView.as_view(), name='event'),
urlpatterns += path(f'{ev_prefix}/<int:pk>/logs/', event.EventLogsView.as_view(), name='event-logs'),
urlpatterns += path(f'{ev_prefix}/form/', event.EventFormView.as_view(), name='event-form'),
urlpatterns += path(f'{ev_prefix}/options/', event.EventOptionList.as_view(), name='event-options'),
urlpatterns += path(f'{ev_prefix}/options/<int:pk>/', event.EventOptionView.as_view(), name='event-option'),

# calendar events
calev_prefix = f'{cal_prefix}/<int:calendar_id>/events'
urlpatterns += path(f'{calev_prefix}/', calendar_event.CalendarEventList.as_view(), name='calendar-events'),
urlpatterns += path(f'{calev_prefix}/<int:pk>/', calendar_event.CalendarEventView.as_view(), name='calendar-event'),
urlpatterns += path(f'{calev_prefix}/<int:pk>/logs/', calendar_event.CalendarEventLogsView.as_view(), name='calendar-event-logs'),
urlpatterns += path(f'{calev_prefix}/form/', calendar_event.CalendarEventFormView.as_view(), name='calendar-events-form'),

# calendar contexts
# publication-contexts
w_prefix = f'{eb_prefix}/sites/<int:site_id>/webpaths'
cc_prefix = f'{w_prefix}/<int:webpath_id>/calendar-contexts'
urlpatterns += path(f'{cc_prefix}/', calendar_contexts.CalendarContextList.as_view(), name='editorial-board-site-webpath-calendar-contexts'),
urlpatterns += path(f'{cc_prefix}/<int:pk>/', calendar_contexts.CalendarContextView.as_view(), name='editorial-board-site-webpath-calendar-context'),
urlpatterns += path(f'{cc_prefix}/<int:pk>/logs/', calendar_contexts.CalendarContextLogsView.as_view(), name='editorial-board-site-webpath-caklendar-context-logs'),
urlpatterns += path(f'{cc_prefix}/form/', calendar_contexts.CalendarContextFormView.as_view(), name='editorial-board-site-webpath-calendar-context-form'),
urlpatterns += path(f'{w_prefix}/calendar-contexts/form/', calendar_contexts.CalendarContextGenericFormView.as_view(), name='editorial-board-site-webpath-calendar-context-form-generic'),
