from django.dispatch import receiver
from django.dispatch import Signal


notification_retrieved = Signal()


@receiver(notification_retrieved)
def see_notification(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.seen = True
    instance.save()
