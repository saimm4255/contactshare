import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import resolve
from .models import AppAccessTime, Contact, ContactView
import logging

logger = logging.getLogger(__name__)




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
        logger.info(f"Middleware triggered for: {request.path}")

        # Check if the user is authenticated and the request is a GET request
        if request.user.is_authenticated and request.method == 'GET':
            try:
                # Use `resolve` to get the URL match
                match = resolve(request.path_info)
                logger.info(f"URL resolved: {match.view_name}")

                # Check if the view name matches the contact detail view
                if match.view_name == 'contact_detail':
                    contact_id = match.kwargs.get('contact_id')
                    logger.info(f"Detected contact_id: {contact_id}")

                    if contact_id:
                        try:
                            contact = Contact.objects.get(id=contact_id)
                            logger.info(f"Contact found: {contact.name}")

                            # Filter JSON serializable metadata from request.META
                            filtered_metadata = {
                                k: v for k, v in request.META.items()
                                if isinstance(v, (str, int, float, bool))  # Only keep serializable data
                            }

                            # Create a ContactView instance
                            ContactView.objects.create(
                                user=request.user, contact=contact, metadata=filtered_metadata
                            )
                            logger.info(f"ContactView created for {contact.name}")
                        except Contact.DoesNotExist:
                            logger.error(f"Contact with id {contact_id} does not exist.")
                        except Exception as e:
                            logger.error(f"Error creating ContactView: {e}")
            except Exception as e:
                logger.error(f"Error resolving URL: {e}")

        # Proceed to the next middleware or view
        response = self.get_response(request)
        return response