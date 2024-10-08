from django import template
from django.utils.timezone import localtime, is_naive
import pytz

register = template.Library()

@register.simple_tag
def display_time_in_timezone(user_time, user_timezone):
    try:
        # If no timezone is provided, default to UTC
        if not user_timezone:
            user_timezone = 'UTC'
        
        # Convert the string to a pytz timezone object
        timezone_obj = pytz.timezone(user_timezone)
        
        # Ensure user_time is a timezone-aware datetime object
        if is_naive(user_time):
            user_time = pytz.UTC.localize(user_time)  # Make user_time timezone-aware in UTC
        
        # Convert the time to the user's timezone
        localized_time = localtime(user_time, timezone_obj)
        
        # Return the formatted time string
        return localized_time.strftime('%Y-%m-%d %H:%M:%S')
    
    except Exception as e:
        return f"Error: {str(e)}"
