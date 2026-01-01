from django import forms
from django.contrib.auth.forms import UserCreationForm#formu widget ile oluşturup değiştirebilmek için htmlde
from django.contrib.auth.models import User
from profiles.models import Profile #profile modelini import etmek
from django.core.exceptions import ValidationError
from .models import ContactMessage

#kullanıcı kaydı formunda özellikleri ve kontolü olan djangonun resgiserformundan usercreation kullanılır 
#ek olarak temaya özel hale getirmek iin widget sınıfı yazılır html de onun sayesinde erişilr
#formun kontrolü şartları sağlaması vs django modulü yapar
class RegisterForm(UserCreationForm):
    email=forms.EmailField(#mail alanı 
        required=True,
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'E-Posta Adresiniz Giriniz'
        })
    )
    first_name=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Adınızı Giriniz'
        })
    )
    last_name=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Soyadınızı Giriniz'
        })
    )
    profession=forms.CharField(
        required=False,#kullanıcı başlangıçta belirtmek zorunda değil
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Mesleğinizi Giriniz(İsteğe Bağlı)'
        })
    )
    profile_image=forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class':'file-control'
        })
    )
    password1=forms.CharField(
        label="Parolanızı Belirleyin",
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Parolanızı Girin'
        })
    )
    password2=forms.CharField(
        label="Parolanızı Doğrulayın",
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Parolanızı Tekrar Girin'
        })
    )
    
    class Meta:
        model=User#modeli oluşturup parametrelerini atama
        fields=['username','email','first_name','last_name','password1','password2']
        
        widgets={
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Kullanıcı Adınızı Belirleyin'
            })
        }
        
    def clean_email(self):#e posta adresninin unique olup olmaması kontrolü
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            #verilen hesabıın modelde olup omladığınının kotnrolü
            raise ValidationError("Bu E-Posta Adresiyle Kayıtlı Kullanıcı Zaten Mevcut")
        return email
    
    #kullanıcıyı kaydettikten sonra güncelleme
    def save(self,commit=True):
        user=super().save(commit)#user uygulama bilgilerini kaydetme
        profession=self.cleaned_data.get('profession')#meslek varsa almak profil modelinden
        profile_image=self.cleaned_data.get('profile_image')
        
        profile=Profile.objects.get(user=user)#kullanıcı bilgilerini alma
        #kaydetme
        
        if profession:#meslek varsa
            profile.profession=profession#meslek varsa onu ayarlama
            
        if profile_image:#profil fotosu varsa
            profile.profile_image=profile_image
        
        #bunlar yoksa bunları boş atar
        profile.save()
        
        return user
    

#loginde ise veritabnına kayıt vs yapılmaz form sınıfından kontrol yapılabilir
#sadece widget tanımlanaır o da temaya uyumlu olabilmesi için

class LoginForm(forms.Form):
    
    username=forms.CharField(
        
        label='Kullanıcı Adı',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Kullanıcı Adınızı Giriniz'
        })
    )
    
    password=forms.CharField(
        label='Parola',
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Parolanızı Giriniz'
        })
    )
    
    
    
    


class UserUpdateForm(forms.ModelForm):
    #profil güncelleme için
    
    username=forms.CharField(
        required=True,
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            "class":"form-control",
           #Form registerda zorunluydu placeholdera gerek yok dolu gelecek zaten
        })
    )
    
    first_name=forms.CharField(
        required=True,
        label="Ad",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            #registerda zorunluydu dğer gelcek db den placeholdera gerek yok
        })
    )
    
    last_name=forms.CharField(
        required=True,
        label="Soyad",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            #registerda zorunlu db den değer gelecek placeholdera gerek yok
        })
    )
    
    email=forms.EmailField(
        required=True,
        label="E-Posta Adresi",
        widget=forms.EmailInput(attrs={
            "class":"form-control",
            #zorunluydu placeholdera gerek yok
        })
    )
    
    
    profession=forms.CharField(
        required=False,
        label="Meslek",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"Mesleğiniz" #kullanıcı girmemiş olabilir veya silmiş olabilir
            #varsa olan gösterilir
        })
    )
    
    bio=forms.CharField(
        required=False,
        label="Biyografi",
        widget=forms.Textarea(attrs={
            "class":"form-control",
            "placeholder":"Hakkınızda kısa bir açıklama",
            "rows":3,
        })
    )
    
    profile_image=forms.ImageField(
        required=False,
        label="Profil Fotoğrafı",
        widget=forms.FileInput(attrs={
            "class":"form-control",
        })
    )
    
    
    twitter_username=forms.CharField(
        required=False,
        label="Twitter Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"Twitter Kullanıcı Adınız",
        })
        
    )
    twitter=forms.URLField(
        required=False,
        label="Twitter Profil Linki",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            "placeholder":"Twitter Profil Bağlantınız"
        })
    )
    
    facebook_username=forms.CharField(
        required=False,
        label="Facebook Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"Facebook Kullanıcı Adınız",
        })
    )
    
    facebook=forms.URLField(
        required=False,
        label="Facebook Porfil Linki",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            "placeholder":"Facebook Profil Bağlantınız",
        })
    )
    
    instagram_username=forms.CharField(
        required=False,
        label="İnstagram Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"İnstagram Kullanıcı Adınız",
        })
    )
    
    instagram=forms.URLField(
        required=False,
        label="İnstagram Profil Linki",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            "placeholder":"İnstagram Profil Bağlantınız",
        })
    )
    
    linkedin_username=forms.CharField(
        required=False,
        label="LinkedIn Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"LinkedIn Kullanıcı Adınız",
        })
    )
    
    linkedin=forms.URLField(
        required=False,
        label="LinkedIn Profil Linki",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            "placeholder":"LinkedIn Profil Bağlantınız",
        })
    )
    
    github_username=forms.CharField(
        required=False,
        label="Github Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"Github Kullanıcı Adınız",
        })
    )
    
    github=forms.URLField(
        required=False,
        label="Github Profil Linki",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            "placeholder":"Github Profil Bağlantınız",
        })
    )
    
    website=forms.URLField(
        required=False,
        label="Kişisel Website Linki",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            "placeholder":"Kişisel Web Sitesi Bağlantınız",
        })
    )
    
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']
        
    
    def __init__(self, *args, **kwargs): #profile bilgilerini olanları doldurmak için
        
        user=kwargs.get('instance')
        super().__init__(*args,**kwargs)
        
        if user and hasattr(user,'profile'):#initial profil bilgileri yükleme
            
            profile=user.profile
            self.fields['profession'].initial=profile.profession
            self.fields['bio'].initial=profile.bio
            self.fields['profile_image'].initial=profile.profile_image
            self.fields['twitter_username'].initial=profile.twitter_username
            self.fields['twitter'].initial=profile.twitter
            self.fields['facebook_username'].initial=profile.facebook_username
            self.fields['facebook'].initial=profile.facebook
            self.fields['instagram_username'].initial=profile.instagram_username
            self.fields['instagram'].initial=profile.instagram
            self.fields['linkedin_username'].initial=profile.linkedin_username
            self.fields['linkedin'].initial=profile.linkedin
            self.fields['github_username'].initial=profile.github_username
            self.fields['github'].initial=profile.github
            self.fields['website'].initial=profile.website
        
        
    
        
    def clean_email(self):#e posta adresninin unique olup olmaması kontrolü
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            #burada kendisi hariç kontrol edilmeli kullanıcı değiştirmeden default ile tamamlarsa 
            #hesap var uyarısı verir

            #verilen hesabıın modelde olup omladığınının kotnrolü
            raise ValidationError("Bu E-Posta Adresiyle Kayıtlı Kullanıcı Zaten Mevcut")
        return email
    
    def save(self, commit=True):
        #user ve profil bilgilerinin aynı anda güncellenmesi
        user=super().save(commit=False)
        
        if commit:
            user.save()
            
            profile=user.profile
            
            profile.profession=self.cleaned_data.get('profession')
            profile.bio=self.cleaned_data.get('bio')
            profile.profile_image=self.cleaned_data.get('profile_image') or profile.profile_image
            profile.twitter_username=self.cleaned_data.get('twitter_username')
            profile.twitter=self.cleaned_data.get('twitter')
            profile.facebook_username=self.cleaned_data.get('facebook_username')
            profile.facebook=self.cleaned_data.get('facebook')
            profile.instagram_username=self.cleaned_data.get('instagram_username')
            profile.instagram=self.cleaned_data.get('instagram')
            profile.linkedin_username=self.cleaned_data.get('linkedin_username')
            profile.linkedin=self.cleaned_data.get('linkedin')
            profile.github_username=self.cleaned_data.get('github_username')
            profile.github=self.cleaned_data.get('github')
            profile.website=self.cleaned_data.get('website')
            
            profile.save()
        
        return user
    
    def clean(self):
        #sosyal medya kullanıcı adları ve linknlerin birlikte girilmesi kontrolü için
        
        
        cleaned_data=super().clean()
        #sosyal medya link eşleşmeleri
        social_pairs= [
            
            ('twitter_username','twitter'),
            ('facebook_username','facebook'),
            ('instagram_username','instagram'),
            ('linkedin_username','linkedin'),
            ('github_username','github')
        ]
        
        for username_field, link_field in social_pairs:
            username=cleaned_data.get(username_field)
            link=cleaned_data.get(link_field)
            
            #eğer herhangi biri dolu diğeri boşsa kullanıcı link
            #hata mesajı 
            
            if (username and not link) or (link and not username):
                
                raise forms.ValidationError(
                    f"{username_field.split('_')[0].title()} alanlarında hem kullanıcı adı hem profil linki birlikte girilemelidir."
                )
                
                

class ContactForm(forms.ModelForm):
    
    class Meta:
        
        model=ContactMessage
        
        fields=['name','email','subject','message']
        
        widgets={
            
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Adınız Soyadınız'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'E-Posta Adresiniz'}),
            'subject':forms.TextInput(attrs={'class':'form-control','placeholder':'Konu'}),
            'message':forms.Textarea(attrs={'class':'form-control','rows':5,'placeholder':'Mesajınızı yazın...'})
        }