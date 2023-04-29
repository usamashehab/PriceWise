from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Product
from django.dispatch import Signal
from favorite.models import Favorite
from django.conf import settings


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    # Update desired_price_reached for related Favorite instances
    favorites = Favorite.objects.filter(
        product=instance, desired_price__gte=instance.price)
    favorites.update(desired_price_reached=True)

    # Send email to users
    emails = list()
    for favorite in favorites:
        user = favorite.user
        emails.append(user.email)

    send_mail(
        subject='Desired price reached',
        message=f'The price for product {instance.title} has reached your desired price.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
    )


product_retrieved = Signal()


@receiver(product_retrieved)
def increase_product_views(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.views += 1
    instance.save()
