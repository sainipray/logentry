from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import CustomLogEntry

User = get_user_model()


class UserListFilter(admin.SimpleListFilter):
    title = _('Users')
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        users = set([log.get_user() for log in model_admin.get_queryset(request)])
        for user in users:
            if isinstance(user.__class__, ModelBase):
                yield (user.pk, user)
            else:
                yield (user, user)

    def queryset(self, request, queryset):
        if self.value():
            try:
                value = int(self.value())
            except ValueError:
                value = self.value()
            if isinstance(value, str):
                return queryset.filter(log_dict__icontains='"user": "{}"'.format(value))
            else:
                return queryset.filter(log__user_id=value)
        else:
            return queryset


class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_link', 'get_content_type_link', 'get_object_id_link', 'get_change_message', 'get_action_flag',
        'get_action_time')

    list_filter = (UserListFilter, 'log__content_type', 'log__action_time')
    search_fields = ('get_user',)

    def get_user_link(self, obj):
        user = obj.get_user()
        if isinstance(user.__class__, ModelBase):
            return mark_safe(
                "<a href='{}' target='_blank'>{}</a>".format(reverse('admin:auth_user_change', args=(user.id,)),
                                                             user.get_full_name() if user.get_full_name() else user.get_username()))
        return user + " (not exist)"

    get_user_link.short_description = "User"

    def get_content_type_link(self, obj):
        model = obj.get_content_type()
        if isinstance(model.__class__, ModelBase):
            return mark_safe(
                "<a href='{}' target='_blank'>{}</a>".format(
                    reverse('admin:{}_{}_changelist'.format(model.app_label, model.model)), model.model.title()))
        return model + " (not exist)"

    get_content_type_link.short_description = "Model Name"

    def get_object_id_link(self, obj):
        obj = obj.get_object_id()
        if isinstance(obj.__class__, ModelBase):
            return mark_safe(
                "<a href='{}' target='_blank'>{}</a>".format(
                    reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name), args=(obj.pk,)),
                    obj.__str__()))
        return obj + " (not exist)"

    get_object_id_link.short_description = "Object"

    readonly_fields = ('get_user', 'get_action_flag', 'get_object_id', 'get_object_repr',
                       'get_content_type', 'get_action_time', 'get_change_message')
    exclude = ('log', 'log_dict',)
    save_as_continue = False
    save_as = False


admin.site.register(CustomLogEntry, LogEntryAdmin)
