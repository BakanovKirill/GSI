# -*- coding: utf-8 -*-
import re

from django.core.exceptions import ValidationError


def validate_order(value):
    """**The method makes the validation of numerical field on a positive number.**

    :Arguments:
        * *value*: Input value

    """

    if value < 0:
        raise ValidationError('{0} invalid value. Must be a positive number'.format(value))

    return value


def validate_lutfile(value):
    """**The method makes the validation of numerical field on a positive number.**

    :Arguments:
        * *value*: Input value

    """

    if value == 'select':
        raise ValidationError('Not a valid LUT File selection.')

    return value


def validate_year(value):
    if not re.match(r'[1-2]{1}[0-9]{3}', value) and len(value) != 4:
        raise ValidationError('Not the correct format of the Year.')

    return value
