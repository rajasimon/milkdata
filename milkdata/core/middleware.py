from django.utils import timezone

from milkdata.core.helper import get_today_date


def DateMiddleware(get_response):
    """
    1. For the first time this middleware sets the "date" to the session.
    """

    def middleware(request):
        if not "date" in request.session:
            request.session["date"] = get_today_date()

        response = get_response(request)
        return response

    return middleware
