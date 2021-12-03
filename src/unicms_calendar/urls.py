from django.urls import path

from cms.api.urls import eb_prefix

from . api.views import (calendar, calendar_event, event)


# CMS_PATH_PREFIX = getattr(settings, 'CMS_PATH_PREFIX', '')
_board_base = 'unicms_calendar'

urlpatterns = []

urlpatterns += path('api/calendars/by-context/<int:webpath_id>/',
                    calendar.ApiContextCalendars.as_view(), name='api-context-calendars'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/<int:pk>/',
                    calendar.ApiContextCalendar.as_view(), name='api-context-calendar'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/events/',
                    calendar.ApiContextCalendarsEvents.as_view(), name='api-context-calendars-events'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/<int:calendar_id>/events/',
                    calendar.ApiContextCalendarEvents.as_view(), name='api-context-calendar-events'),
urlpatterns += path('api/calendars/by-context/<int:webpath_id>/<int:calendar_id>/events/<int:pk>/',
                    calendar.ApiContextCalendarEvent.as_view(), name='api-context-calendar-event'),

# calendars
cal_prefix = f'{eb_prefix}/calendars'
urlpatterns += path(f'{cal_prefix}/',
                    calendar.CalendarList.as_view(), name='calendars'),
urlpatterns += path(f'{cal_prefix}/<int:pk>/',
                    calendar.CalendarView.as_view(), name='calendar'),
urlpatterns += path(f'{cal_prefix}/<int:pk>/logs/',
                    calendar.CalendarLogsView.as_view(), name='calendar-logs'),
urlpatterns += path(f'{cal_prefix}/form/',
                    calendar.CalendarFormView.as_view(), name='calendar-form'),
urlpatterns += path(f'{cal_prefix}/options/',
                    calendar.CalendarOptionList.as_view(), name='calendar-options'),
urlpatterns += path(f'{cal_prefix}/options/<int:pk>/',
                    calendar.CalendarOptionView.as_view(), name='calendar-option'),

# events
ev_prefix = f'{eb_prefix}/events'
urlpatterns += path(f'{ev_prefix}/', event.EventList.as_view(), name='events'),
urlpatterns += path(f'{ev_prefix}/<int:pk>/',
                    event.EventView.as_view(), name='event'),
urlpatterns += path(f'{ev_prefix}/<int:pk>/logs/',
                    event.EventLogsView.as_view(), name='event-logs'),
urlpatterns += path(f'{ev_prefix}/form/',
                    event.EventFormView.as_view(), name='event-form'),
urlpatterns += path(f'{ev_prefix}/options/',
                    event.EventOptionList.as_view(), name='event-options'),
urlpatterns += path(f'{ev_prefix}/options/<int:pk>/',
                    event.EventOptionView.as_view(), name='event-option'),

# calendar events
calev_prefix = f'{cal_prefix}/<int:calendar_id>/events'
urlpatterns += path(f'{calev_prefix}/',
                    calendar_event.CalendarEventList.as_view(), name='calendar-events'),
urlpatterns += path(f'{calev_prefix}/<int:pk>/',
                    calendar_event.CalendarEventView.as_view(), name='calendar-event'),
urlpatterns += path(f'{calev_prefix}/<int:pk>/logs/',
                    calendar_event.CalendarEventLogsView.as_view(), name='calendar-event-logs'),
urlpatterns += path(f'{calev_prefix}/form/',
                    calendar_event.CalendarEventFormView.as_view(), name='calendar-events-form'),
# urlpatterns += path(f'{calev_prefix}/options/', calendar_event..CalendarEventOptionList.as_view(), name='calendar-event-options'),
# urlpatterns += path(f'{calev_prefix}/options/<int:pk>/', calendar_event..CalendarEventOptionView.as_view(), name='calendar-event-option'),
