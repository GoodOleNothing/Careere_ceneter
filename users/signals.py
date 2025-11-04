from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import User
import os


@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_avatar = User.objects.get(pk=instance.pk).avatar
    except User.DoesNotExist:
        return

    new_avatar = instance.avatar
    if old_avatar and old_avatar != new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)


@receiver(post_delete, sender=User)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

