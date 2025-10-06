import requests
from celery.bin.upgrade import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from pyexpat.errors import messages

# from products.tasks import send_telegram_notification
from products.models.order import Order
#
@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.CHAT_ID
        method = 'sendMessage'
        message_text = f"New Order: {instance.id}\n Product: {instance.product.name}\n Quantity {instance.quantity}" +\
            f"\nClient: {instance.customer.username}\n tel: {instance.phone_number}"

        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/{method}',
            data={'chat_id':chat_id, 'text':message_text}
        ).json()



