from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ProfileViewSet, ContactViewSet
from django.contrib.auth import views as auth_views  
from .forms import CustomAuthenticationForm  
from . import views

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('contact/edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('contact/delete/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('stats/', views.stats, name='stats'),
]
