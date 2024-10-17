# your_app/decorators.py

from functools import wraps

def log_request_metadata(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Print request metadata
        metadata = request.META
        print(f"Request Metadata: {metadata}")
        return view_func(request, *args, **kwargs)
    
    return wrapper
