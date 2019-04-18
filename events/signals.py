from django.db.models.signals import post_save, pre_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Event, Invitation
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import os


'''
@receiver(post_save, sender=Event)
def rsvp_host(sender, instance, created, **kwargs):
    if created:
        host = instance.host
        Invitation.objects.create(event=instance, guest=host, replied=True, attending=True)
'''


@receiver(m2m_changed, sender=Event.guests.through)
def create_invitations(sender, instance, action, **kwargs):
    if action == 'post_remove':
        for invitation in Invitation.objects.filter(event=instance):
            if not invitation.guest in instance.guests.exclude(id=instance.host.id):
                Invitation.objects.filter(event=instance, guest=invitation.guest).delete()
    if action == 'post_add':
        for guest in instance.guests.all():
            if not Invitation.objects.filter(event=instance, guest=guest).exists():
                Invitation.objects.create(event=instance, guest=guest)
                mail_subject = 'hosTable: Invitation to ' + str(instance)
                domain = os.environ.get("HOSTABLE_SITE")
                message = render_to_string('invitation_email.html', {
                    'user': guest,
                    'event': instance,
                    'domain': domain,
                })
                to_email = guest.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = "html"
                email.send()
