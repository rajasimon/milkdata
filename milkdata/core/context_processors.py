from milkdata.core.helper import get_today_date


def inject_today(request):
    return {"today": get_today_date()}
