from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

def updateuser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False: 
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()



#@receiver(post_delete, sender=Profile)
def userDelete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender=User)
post_delete.connect(updateuser, sender=Profile) #sender means that the signal comes from profile
post_delete.connect(userDelete, sender=Profile)