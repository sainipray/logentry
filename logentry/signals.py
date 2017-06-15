#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers


def save_user_log(sender, instance, *args, **kwargs):
    from django.contrib.auth import get_user_model
    from .models import CustomLogEntry
    User = get_user_model()
    user = User.objects.get(id=instance.user.id)
    user = user.get_full_name() if user.get_full_name() else user.get_username()
    data = serializers.serialize("json", [instance])
    data = json.loads(data)[0]['fields']
    data['user'] = user
    clm = CustomLogEntry(log=instance, log_dict=json.dumps(data))
    clm.save()
