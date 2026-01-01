#Kullanıcı profile oluştuduğunda otomatik bağlantı için kullanılır

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

#Kullanıcı oluşturulduğunda profil uygulamasını da ona bağlı olarak otomatik oluşturma

@receiver(post_save, sender=User)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
#kullanıcı kaydedildiğinde profili de kaydetme

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
    
#post_save user modeli üzerinden her kullanıcı oluştuğunda tetiklenir created bunun ilk kez olup olmadığına 
#olmadığına bakar ilk kez ise kayıttır değilse güncellemedir

#SİNYAL DJANGOYU TANITILIR profiles/app.py