from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('contact/edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('contact/delete/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
