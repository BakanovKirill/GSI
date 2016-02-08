# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from gsi.models import (CardSequence)
from cards.models import CardItem


def cs_cards_update(form, cs_card, card_item):
    cs_card.order = form.cleaned_data["order"]
    cs_card.card_item = card_item
    cs_card.save()

    return cs_card
