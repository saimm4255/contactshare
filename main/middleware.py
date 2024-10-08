import datetime
from django.utils import timezone
from django.shortcuts import redirect
from .models import AppAccessTime, Contact, ContactView

class AccessTimeRestrictionMiddleware: 
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Fetch the active access time
        active_time = AppAccessTime.objects.filter(is_active=True).first()

        if active_time:
            now = timezone.localtime(timezone.now()).time()

            # Restrict access based on specified access time
            if not (active_time.from_time <= now <= active_time.to_time):
                return redirect('access_denied')

        response = self.get_response(request)
        return response



class ContactViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.method == 'GET':
            # Ensure resolver_match is not None
            if request.resolver_match:
                contact_id = request.resolver_match.kwargs.get('contact_id')

                # Only track contact views if contact_id exists
                if contact_id:
                    try:
                        contact = Contact.objects.get(id=contact_id)
                        ContactView.objects.create(
                            user=request.user, contact=contact, metadata=request.META
                        )
                    except Contact.DoesNotExist:
                        pass  # In case the contact does not exist
                        
        response = self.get_response(request)
        return response
