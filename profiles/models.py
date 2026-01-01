from django.db import models
from django.contrib.auth.models import User #bağlı olacğı uygulmayı ekleme
# Create your models here.

#PRofile uygulmasının ayrı oluşturulmasının sebebi
""" Kullanıcının doldurmadan da kayıt olabileceği bilgilerle 
Hayati bilgileri ayırmak . Kullanıcı bunları sonradan dğeiştirebilir.
Böylelikle kullanımı ve kontrolü kolay bir mimari oluşur
    """

class Profile(models.Model):
    
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    #bir e bir ilişki olcağından belirlendi silinince ona ait veriler de silinmesi ayarlandı CASCADE ile
    
    
    profession=models.CharField(max_length=100, blank=True, null=True)#meslek
    #kullanıcı bunu belirtmeden girebilir
    profile_image=models.ImageField(upload_to='profile_pics/',default='profile_pics/default.jpg',blank=True,null=True)
    #profil fotoğrafı
    
    bio=models.TextField(blank=True,null=True)
    #bio
    twitter_username=models.CharField(max_length=50,blank=True,null=True)
    twitter=models.URLField(blank=True,null=True)
    
    facebook_username=models.CharField(max_length=50,blank=True,null=True)
    facebook=models.URLField(blank=True,null=True)
    
    instagram_username=models.CharField(max_length=50,blank=True,null=True)
    instagram=models.URLField(blank=True,null=True)
    
    linkedin_username=models.CharField(max_length=50,blank=True,null=True)
    linkedin=models.URLField(blank=True,null=True)
    
    github_username=models.CharField(max_length=50,blank=True,null=True)
    github=models.URLField(blank=True,null=True)
    
    website=models.URLField(blank=True,null=True)
    
    #kayıt esannasında sorulmayıp güncellemeyle kelencek bilgiler bio ve sosyal medya linkleri
    
    
    def __str__(self):
        return f"{self.user.username} Profile" #admin panelinde kullanıcı adını gösterebilmek için
    