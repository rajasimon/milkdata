from django import template
from django.db.models import Sum

register = template.Library()


@register.filter
def shed_data_sum(qs):
    if qs:
        aggregation = qs.aggregate(Sum("value"))
        return round(aggregation["value__sum"], 3)
    return 0


@register.filter
def get_date_data_half_litre(qs, date):
    shop_data = qs.filter(date=date).first()
    if shop_data:
        return shop_data.half_litre

    return None


@register.filter
def get_date_data_quarter_litre(qs, date):
    shop_data = qs.filter(date=date).first()
    if shop_data:
        return shop_data.quarter_litre

    return None


@register.filter
def get_date_data_tray(qs, date):
    shop_data = qs.filter(date=date).first()
    if shop_data:
        return shop_data.tray

    return None


@register.filter
def get_date_data_additional(qs, date):
    shop_data = qs.filter(date=date).first()
    if shop_data:
        return shop_data.additional

    return None


@register.filter
def calculate_litre(qs, date):
    shop_data = qs.filter(date=date).first()
    total_litre = 0
    if shop_data:
        if shop_data.half_litre:
            total_litre += shop_data.half_litre / 2

        if shop_data.quarter_litre:
            total_litre += shop_data.quarter_litre / 4

        if shop_data.additional:
            total_litre += shop_data.additional
    return total_litre
