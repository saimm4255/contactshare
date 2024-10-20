from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from rest_framework import viewsets, permissions
from .models import Contact, Profile, ContactView, CustomUser
from .serializers import CustomUserSerializer, ProfileSerializer, ContactSerializer
from .forms import SignUpForm, ProfileUpdateForm, ContactForm
from .decorators import log_request_metadata



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@log_request_metadata
@login_required
def home(request):
    all_contacts = Contact.active_objects.all()
    my_contacts = Contact.active_objects.filter(user=request.user)
    return render(request, 'home.html', {'all_contacts': all_contacts, 'my_contacts': my_contacts})

@log_request_metadata
@login_required
def stats(request):
    overall_views = ContactView.objects.filter(contact__user=request.user).count()
    most_viewed_contact = Contact.objects.filter(user=request.user).annotate(view_count=Count('contactview')).order_by('-view_count').first()
    least_viewed_contact = Contact.objects.filter(user=request.user).annotate(view_count=Count('contactview')).order_by('view_count').first()
    views_by_country = ContactView.objects.values('metadata__REMOTE_ADDR').annotate(total_views=Count('id')).order_by('-total_views')
    contacts_ordered_by_views = Contact.objects.filter(user=request.user).annotate(view_count=Count('contactview')).order_by('-view_count')
    average_views_per_contact = ContactView.objects.filter(contact__user=request.user).aggregate(average_views=Avg('id'))

    context = {
        'overall_views': overall_views,
        'most_viewed_contact': most_viewed_contact,
        'least_viewed_contact': least_viewed_contact,
        'views_by_country': views_by_country,
        'contacts_ordered_by_views': contacts_ordered_by_views,
        'average_views_per_contact': average_views_per_contact,
    }
    return render(request, 'stats.html', context)

@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    total_views = ContactView.objects.filter(contact=contact).count()

    context = {
        'contact': contact,
        'total_views': total_views,
    }
    return render(request, 'contact_detail.html', context)

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'add_contact.html', {'form': form})

@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'edit_contact.html', {'form': form, 'contact': contact})

@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('home')

    return render(request, 'delete_contact.html', {'contact': contact})

def access_denied(request):
    return render(request, 'main/access_denied.html', {})
