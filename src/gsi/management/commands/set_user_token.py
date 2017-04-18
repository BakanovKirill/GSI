# -*- coding: utf-8 -*-
import requests

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
	def handle(self, *args, **options):
		for us in User.objects.all():
			Token.objects.get_or_create(user=us)
