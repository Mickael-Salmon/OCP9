from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a Profile object whenever a new User is created.

    Parameters:
        sender (Model): The model class that sent the signal.
        instance (Model instance): The instance of the model.
        created (bool): True if a new record was created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Save the profile whenever the corresponding User object is saved.

    Parameters:
        sender (Model): The model class that sent the signal.
        instance (Model instance): The instance of the model.
    """
    instance.profile.save()
