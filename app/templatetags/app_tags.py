from django import template

register = template.Library()

from app.misc import blocodata_properties


@register.simple_tag
def blocodata_calculated_fields(blocodata):
    """ Retorna uma lista de tuples com todos as propriedades de Blocodata"""

    return [
        (field[0], getattr(blocodata, field[0]))
            for field in blocodata_properties
    ]
