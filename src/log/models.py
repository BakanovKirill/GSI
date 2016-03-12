from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
	""" system logs """
	user = models.ForeignKey(User)
	element = models.CharField(max_length=15, null=False, db_index=True)  # element model
	element_id = models.IntegerField(null=False, db_index=True)  # element id
	message = models.TextField(null=False, default='')
	at = models.DateTimeField(auto_now_add=True, null=False)

	def __unicode__(self):
		return u'%s' % self.message[:25]
