from django.utils import timezone

def current_user_info(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        user_timezone = profile.timezone if profile else 'UTC'
        return {
            'current_time': timezone.now(),
            'current_user': request.user,
            'user_timezone': user_timezone
        }
    return {}
