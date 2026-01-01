from django.shortcuts import render,redirect
from .forms import LoginForm#formların import edilmesi
from .forms import RegisterForm ,UserUpdateForm  

from django.contrib.auth.models import User
#kullanıcı biglilerinin ayarlanması için import etme
#nesen türetilir

from django.contrib.auth import login,authenticate,logout
#başarılı  kayıttan sonra kullanıcnın sisteme direkt girmesini sağlar

from django.contrib import messages#django mesajları için 
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django_ratelimit.decorators import ratelimit

from core.views import error_429_view  # en üste import et




# Create your views here.
@ratelimit(key='ip', rate='3/m', block=True)
def register(request):#oluşturulan formun gösterilmesi
    
    #mantık olaarak aynı request post ise kayıt işlemleri değilse sadece görüntülemedir
    #formu göstermek gerekir 
    
    if getattr(request,'limits',False):
        return error_429_view(request)
    #Djangonun tanıdığı kolaylık
    
    """
        -Form nesnesi oluştur
        -Form nesnesi pos iken göster yoksa none şeklinde göster
        (get request ise none gelir post gösterilmez post ise none gelmez)Uzun if bloklarından kurtuldun
        
        -- Doğruluk kontrolü  yap ve kaydetme işlemlerini gerçekleştir
        --Get request olmadığında veya valid yanlışken context ile formu göster
        
    
    """
    
    form=RegisterForm(request.POST or None , request.FILES or None)
    #registerformdan istek postsa fotoğraf gelmişse bilgielri vs alır
    
    if form.is_valid():
        
        #hem user hem profile oluşturulur
        
        user = form.save()

        
        #eğer profil fotoğrafı veya meslek girilmemişse defuault bilgilerle oluşturulur
        
        form.save_m2m()#ileride many to many ilişkiye karşın güvenlik için
        
        login(request,user)#giriş ekranı
        messages.success(request,"Kayıt işlemi başarılı! Hoşgeldiniz...")
        return redirect("index")#kayot işlemi sornası index
    
    #form geçerli olmayabilir veya kullanıcı sadece get request atmış olabilir
    
    return render(request,"register.html",{"form":form})#form ve register sayfası dönülür
    
    
    
    #MANTIK
    """
        Gelen işlem post mu get mi kotnrol et:
        Eğer Post ise:
             
            -form bilgilerini al ve doldur
            -daha sonra gelen bilgilerin doğruluğunu kontrol et
            -doğruysa yeni kullanıcı oluştur ve bilgileri gönder
            -kullanıcıyı kaydet save ile login ile sisteme giriş yaptır
        
        İşlem başarılı olmadıysa tekrar indexe yönlendir form bilgierlini doldurt
        
        Post değilse
             
             - from bilgilerini  göster gettir istek
    
    """
    #Bu işlem çok uzun olabilir altrnatif ise yukarıda
    #--------------------------------------------------------------------------------------
    """
    if request.method=="POST":
        #işlem post ise gelen bilgilerle formu doldurmak gerekir
        
        form=RegisterForms(request.POST)
        #biglilerle doludrma
        #form is valid yani form tamam mı işlemi sağlanırsa değerleri dödnürür
        
        if form.is_valid():#form kontrolü tamamsa
            #clean metodundan alınır
            
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            #bilgiler alındı
            #obje oluştur kaydet
            
            newUser=User(username=username)#kullanıcı bilgilerinin ayarlanması
            newUser.set_password(password)
            #veritabanına kaydı
            newUser.save()
            login(request,newUser)#başarılı kayıttan sonra doğrudan giriş yapmayı sağlayan yer
            
            return redirect("index")#doğrudan gideceği link
            

        context={
            "form":form
        }
        return render(request,"register.html",context)
        
    else:
        form=RegisterForms()
        context={
            "form":form
        }
        return render(request,"register.html",context)
    
    
    form=RegisterForms() # form türetme
    
    context={#oluşturlan içerik
        "form": form
    }
    
    return render(request,"register.html",context)#context ile gönderme"""
#----------------------------------------------------------------------------------------------

@ratelimit(key='ip', rate='5/m', block=True)
def loginUser(request):
    
    #form oluştur 
    #context ile içeirkleri oluştur
    
    if getattr(request,'limits',False):
        
        return error_429_view(request)
    
    form=LoginForm(request.POST or None)
    
    context={
        "form":form
    }
    if form.is_valid():#form doğru domuşsa giriş yapılır
        
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        
        #forms.py de clean işlemi var override yağmadığımız için default gelir
        
        #username ve password bilgisine göre sorgu yapılması için login kullan
        #authenticate metodu kullanıcının biglgilerini alır kontrol eder ve geri döner
        
        user=authenticate(username=username,password=password)
        #kullanıcnın olup olmadığı bilgisi user a atandı
        
        if user is None:
            #kullanıcı yoksa
            
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı!Tekrar Deneyiniz...")
            
            return render(request,"login.html",context)#hata mesajıyla başa döndrü ve contexti gönder
        
        
            #kullanıcı varsa
        messages.success(request,"Giriş Başarılı!!!")
        login(request,user)#kullanıcıyı siteme giriş yaptrı
            
        return redirect("index")
    #form is valid değilse yani doğru değil ya da istek get ise
    
    return render(request,"login.html",context)

    
    

def logoutUser(request):
    logout(request)
    messages.success(request,"Çıkış Başarılı!Görüşmek Üzere")
    #bu şekilde logout  fonksiyonuna bilgiler verilerek çıkış yapılır giriş request te var zaten
    return redirect("index")





@login_required(login_url="user:login")
def update_profile(request):
    
    user=request.user
    #aktif kullanıcı alınması
    
    if request.method=="POST":#form doldurulmuşsa
        
        form=UserUpdateForm(request.POST , request.FILES, instance=user)
        if form.is_valid(): #şartları sağladıysa
            
            form.save()
            
            messages.success(request,"Porfil Güncelleme Başarılı")
            
            return redirect("article:dashboard")
        
        else:
            messages.info(request,"Formda Hatalı Alalar Mevcut!!!")
            
        
    else:
        form=UserUpdateForm(instance=user)#aksi halde sayfa görüntülemedir GET bilgileri doldur ver
        
    
    context={
        "form":form
    }
    
    return render(request,"update_profile.html",context)
        
        
@ratelimit(key='ip', rate='2/m', block=True)
def contact(request):
    
    if getattr(request,'limits',False):
        
        return error_429_view(request)
    
    if request.method=='POST':
        form=ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            messages.success(request,"Mesaj iletimi başarılı. İletişime geçtiğiniz için teşekkürler")
            return redirect("user:contact")
        else:
            messages.info(request,"Lütfen formu kontrol edin. Gerekli alanlar olabilir!!!")
        
    
    else:
        
        form=ContactForm()
        
    return render(request,"contact.html",{"form":form})