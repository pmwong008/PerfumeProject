from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import CustomUser
from admin_app.profiles import UserProfile

@receiver(post_delete, sender=CustomUser)
def delete_user_profile(sender, instance, **kwargs):
    profile = UserProfile.objects(user_id=instance.id)
    if profile:
        profile.delete()

    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
