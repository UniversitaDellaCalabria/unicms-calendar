
from cms.api.permissions import UNICMSUserGetCreatePermissions


class CalendarGetCreatePermissions(UNICMSUserGetCreatePermissions):
    """
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, 'unicms_calendar', 'calendar')


class EventGetCreatePermissions(UNICMSUserGetCreatePermissions):
    """
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, 'unicms_calendar', 'event')
