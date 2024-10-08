from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Contact, Profile
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileUpdateForm,  ContactForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


def access_denied(request):
    return render(request, 'main/access_denied.html', {})
    
@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    if request.method == 'POST':
        contact.delete()
        return redirect('home')
    
    return render(request, 'delete_contact.html', {'contact': contact})


@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after editing
    else:
        form = ContactForm(instance=contact)

    return render(request, 'edit_contact.html', {'form': form, 'contact': contact})

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user  # Associate the contact with the logged-in user
            contact.save()
            return redirect('home')  # Redirect to the home page after adding contact
    else:
        form = ContactForm()

    return render(request, 'add_contact.html', {'form': form})

# Sign Up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Home view
@login_required
def home(request):
    all_contacts = Contact.active_objects.all()
    my_contacts = Contact.active_objects.filter(user=request.user)
    return render(request, 'home.html', {'all_contacts': all_contacts, 'my_contacts': my_contacts})

# View Profile
@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

# Update Profile
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

# Contact Detail
@login_required
def contact_detail(request, contact_id):
    contact = Contact.active_objects.get(id=contact_id)
    return render(request, 'contact_detail.html', {'contact': contact})
