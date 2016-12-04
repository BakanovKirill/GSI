from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
	"""**Model for the system logs.**

    :Fields:

        **user**: Current user

        **element**: Model name

        **element_id**: Element model id

        **message**: Message for the log file

        **at**: Date create

    """

	user = models.ForeignKey(User)
	element = models.CharField(max_length=15, null=False, db_index=True)  # model name
	element_id = models.IntegerField(null=False, db_index=True)  # element model id
	message = models.TextField(null=False, default='')
	at = models.DateTimeField(auto_now_add=True, null=False)

	def __unicode__(self):
		return u'%s' % self.message[:25]


class LogDebug(models.Model):
	"""**Model for the debug logs.**

    :Fields:

        **name**: Object name

        **log**: Message for the log file

        **create_date**: Date create

    """

	name = models.CharField(max_length=100)
	log = models.TextField(blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.name
