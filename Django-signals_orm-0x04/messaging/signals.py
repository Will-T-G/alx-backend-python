from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only run for existing messages (not new ones)
    if not instance.pk:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Content changed?
    if old.content != instance.content:
        # Save old content to history
        MessageHistory.objects.create(
            message=instance,
            old_content=old.content,
            editor=instance.sender,  # You can adjust if needed
        )

        # Flag message as edited
        instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Clean up all user-related data when the user account is deleted.
    Triggered automatically after a User is deleted.
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(user=instance).delete()
