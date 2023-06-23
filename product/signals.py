
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from django.dispatch import Signal
from favorite.models import Favorite
from django.conf import settings
from notification.models import Notification
from django.utils import timezone
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    update_desired_price_reached(instance)
    favorites = get_matching_favorites(instance)

    notifications = create_notifications(instance, favorites)
    Notification.objects.bulk_create(notifications)

    send_price_alert_emails(instance, favorites)


def update_desired_price_reached(instance):
    favorites_1 = Favorite.objects.filter(
        notify_when_any_drop=False, product=instance, desired_price__gte=instance.price).select_related('user')
    favorites_1.update(price_change_notified=True)

    favorites_2 = Favorite.objects.filter(
        notify_when_any_drop=True, product=instance, last_notified_price__gte=instance.price).select_related('user')
    favorites_2.update(price_change_notified=True,
                       last_notified_price=instance.price)


def get_matching_favorites(instance):
    favorites_1 = Favorite.objects.filter(
        notify_when_any_drop=False, product=instance, desired_price__gte=instance.price)
    favorites_2 = Favorite.objects.filter(
        notify_when_any_drop=True, product=instance, last_notified_price__gte=instance.price)
    return favorites_1 | favorites_2


def create_notifications(instance, favorites):
    notifications = []
    for favorite in favorites:
        user = favorite.user
        notification_title = f'Price of {instance.title} has dropped to {instance.price}. Hurry up and buy it.'
        notification = Notification(
            user=user, favorite=favorite, title=notification_title)
        notifications.append(notification)
    return notifications


def send_price_alert_emails(instance, favorites):
    emails = favorites.values_list('user__email', flat=True)
    subject = 'Price Alert'
    context = {'product': instance}
    email_body = render_to_string('email/price_alert.html', context)

    email_message = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[],
        bcc=emails
    )
    email_message.content_subtype = 'html'
    email_message.send()


product_retrieved = Signal()


@receiver(product_retrieved)
def increase_product_views(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.views += 1
    instance.updated_at = timezone.now()
    instance.save()
