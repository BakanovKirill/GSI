from django import template

from gsi.settings import CARD_TYPE


register = template.Library()

@register.filter(name='type')
def card_type(value):
    """Get type for the card."""
    return CARD_TYPE[value]
