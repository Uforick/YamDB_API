import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    max_year = datetime.date.today().year + 10
    params = {'value': max_year}
    message_g = _('Введите год меньше, чем %(value)s')
    message_l = _(
        'Введите год больше или равный -2600 ("-" для года до н.э.), '
        'но не более %(value)s'
    )
    if value > max_year:
        raise ValidationError(message=message_g, params=params)
    elif value < -2600:
        raise ValidationError(message=message_l, params=params)
