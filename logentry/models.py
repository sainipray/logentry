import json

from django.contrib.admin.models import LogEntry
from django.db import models
from django.db.models.signals import post_save
from django.utils.dateparse import parse_datetime
from django.utils.translation import ugettext_lazy as _

from logentry.signals import save_user_log

ADDITION = 1
CHANGE = 2
DELETION = 3


class CustomLogEntry(models.Model):
    log = models.OneToOneField(LogEntry, verbose_name=_('Logs'), null=True, blank=True,
                               on_delete=models.SET_NULL)
    log_dict = models.TextField(verbose_name=_(
        'It will save all entries of Log model Instance.'
        ' If user deleted then that data will show to user information in admin'))

    class Meta:
        verbose_name = _('Log Entry')
        verbose_name_plural = _('Log Entries')

    def __str__(self):
        return "{} user {} {} object".format(self.get_user(), self.get_action_flag(), self.get_content_type())

    def __unicode__(self):
        return self.__str__()

    def get_data(self, key):
        if self.log:
            return getattr(self.log, key)
        else:
            return json.loads(self.log_dict)[key]

    def get_action_flag(self):
        flag = self.get_data('action_flag')
        if flag == ADDITION:
            return "added"
        elif flag == CHANGE:
            return "changed"
        elif flag == DELETION:
            return "deleted"

    get_action_flag.short_description = _('Action Flag')

    def get_action_time(self):
        action_time = self.get_data('action_time')
        if self.log:
            return action_time
        else:
            return parse_datetime(action_time)

    get_action_time.short_description = _('Action Time')

    def get_change_message(self):
        if self.log:
            return self.log.__str__()
        return self.get_data('change_message')

    get_change_message.short_description = _('Message')

    def get_content_type(self):
        from django.contrib.contenttypes.models import ContentType
        data = self.get_data('content_type')
        if isinstance(data, ContentType):
            return data
        return ContentType.objects.get(id=data)

    get_content_type.short_description = _('Model Name')

    def get_object_id(self):
        model = self.get_content_type()
        obj = self.get_data('object_id')
        try:
            pk_name = model._meta.pk.name
            kw = {pk_name: obj}
            return model.model_class().objects.get(**kw)
        except model.DoesNotExist:
            return obj

    get_object_id.short_description = _('Object')

    def get_object_repr(self):
        return self.get_data('object_repr')

    get_object_repr.short_description = _('Object repr')

    def get_user(self):
        return self.get_data('user')

    get_user.short_description = _('User')


post_save.connect(save_user_log, LogEntry, dispatch_uid='save_user_log')
