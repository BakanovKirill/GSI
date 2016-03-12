# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User

from log.models import Log


def log_it(user, element, element_id, message):
	""" message write message to the element element to the log """

	Log.objects.create(
		user=user or User.objects.get(id=1),
		element=element,
		element_id=element_id,
		message=message,
		at=datetime.now(),
	)


def get_logs(element, element_id, limit=None, user=None):
	""" get the log messages for the element element """

	logs = Log.objects.filter(element=element, element_id=element_id).order_by('-at')

	if user is not None:
		logs = logs.filter(user=user)

	if limit:
		logs = logs[:limit]

	return logs