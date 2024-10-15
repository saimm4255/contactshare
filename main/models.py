from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=100, default='UTC')
    picture = models.ImageField(upload_to='profile_pics/', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)

    objects = models.Manager() 
    active_objects = ActiveManager() 


class AppAccessTime(models.Model):
    from_time = models.TimeField()
    to_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
     
        unique_together = ('id',)

    def __str__(self):
        return f"Access Time from {self.from_time} to {self.to_time}"

class ContactView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    metadata = models.JSONField()  

    def __str__(self):
        return f"{self.user.username} viewed {self.contact.name}"





