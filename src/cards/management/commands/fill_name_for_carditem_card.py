# -*- coding: utf-8 -*-
import requests

from django.core.management.base import BaseCommand

from cards.models import CardItem


class Command(BaseCommand):
	def handle(self, *args, **options):
		card_items = CardItem.objects.all()

		for card in card_items:
			card.name = u"{0}".format(card.content_object)
			card.save()
