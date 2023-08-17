import logging

from account.models import Profile


def header(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception as E:
            logging.warning(f"{E}")
    return {'profile': profile}