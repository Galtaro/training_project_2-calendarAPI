from django.contrib import admin
from django.contrib.admin.options import get_content_type_for_model
from rest_framework.exceptions import ValidationError

from events.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["value_time", "description"]
    ordering = ["value_time"]

    def log_deletion(self, request, obj, object_repr):

        from django.contrib.admin.models import DELETION, LogEntry

        """
        Prevents the administrator from deleting an entry in the Notification table with id=1,
        the value of which makes it possible not to send a notification to user
        """

        if obj.id == 1:
            raise ValidationError({
                "detail": "You cannot delete this entry"
            }, code='invalid')

        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=object_repr,
            action_flag=DELETION,
        )


admin.site.register(Notification, NotificationAdmin)
