from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save,sender=User)
def user_postsave(sender, instance, created, **kwargs):
  user = instance
  
  # Add profile is the user is created
  if created:
    Profile.objects.create(user=user)
    
     # Cria um EmailAddress inicial se ainda não existir
    EmailAddress.objects.get_or_create(
      user=user,
      email=user.email,
      defaults={
        'primary': True, 
        'verified': False,
        }
      )
    
  else:
    # update allauth emailaddress is exist
    try:
      email_address = EmailAddress.objects.get(user=user, primary=True)
      if email_address != user.email:
        email_address.email = user.email
        email_address.verified = False
        email_address.save()  
    
    except EmailAddress.DoesNotExist:
      # if emailaddress don't exist, create one
      EmailAddress.objects.create(
        user = user,
        email = user.email,
        primary = False,
        verified = False,        
      )
      
@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
  if instance.username:
    instance.username = instance.username.lower()