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
    vendor_data = qs.filter(date=date).first()
    if vendor_data:
        return vendor_data.half_litre

    return None


@register.filter
def get_date_data_quarter_litre(qs, date):
    vendor_data = qs.filter(date=date).first()
    if vendor_data:
        return vendor_data.quarter_litre

    return None


@register.filter
def get_date_data_note(qs, date):
    vendor_data = qs.filter(date=date).first()
    if vendor_data:
        return vendor_data.note

    return None


@register.filter
def get_date_data_additional(qs, date):
    vendor_data = qs.filter(date=date).first()
    if vendor_data:
        return vendor_data.additional

    return None


@register.filter
def calculate_litre(qs, date):
    vendor_data = qs.filter(date=date).first()
    total_litre = 0
    if vendor_data:
        if vendor_data.half_litre:
            total_litre += vendor_data.half_litre / 2

        if vendor_data.quarter_litre:
            total_litre += vendor_data.quarter_litre / 4

        if vendor_data.additional:
            total_litre += vendor_data.additional
    return total_litre
