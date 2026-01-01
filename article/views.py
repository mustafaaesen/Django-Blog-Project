from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForms# formdaki articleformdan nesne alabilmek için
from django.contrib import messages
from . models import Article,Comment,ArticleLike,CommentLike
from django.contrib.auth.decorators import login_required#giriş kontrolü için
from profiles.models import Profile
from django.http import JsonResponse
from django.core.paginator import Paginator
import math
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.db.models import Count, F, Value, IntegerField
from django.db.models.functions import Coalesce
from django_ratelimit.decorators import ratelimit

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.views import error_429_view


# Create your views here.
def index(request):#urls py deki linkin fonksiyonları yazılrı request atılrı 
    
    #anasayfada göstermek için en popüler 5 makale ve son 5 makale 
    
    #son 5
    
    latest_articles=(
        Article.objects.select_related('author__profile').order_by('-created_date')[:5]
    )
    #en popüler 5 en çok beğeni ve yorum alanlar
    
    popular_articles=(
        Article.objects.select_related('author__profile').annotate(
            total_engagement=Count('likes',distinct=True) + Count('comments',distinct=True)
        ).order_by('-total_engagement','-created_date')[:5]
    )
    
    for article in list(latest_articles) + list(popular_articles):
        word_count=len(article.content.split())
        article.reading_time=math.ceil(word_count/200) #dk cinsinden ortalama okuma süresi hesabı
        
    context={
        "latest_articles":latest_articles,
        "popular_articles":popular_articles,
    }
    
    return render(request,"index.html", context)# http response ya da template döner
    #buradaki fonksiyon tekrar blog->urls.py de dahil edilir
    
    
def about(request):
    #en popüler yazarları göstermek için yazılan fonksşyon
    
    top_authors=( # en popüler 3 yazarı makale sayısı beğenisi yorum beğenisi yorumları aracılığıyla bulmak
        
        Profile.objects.annotate(
            
            article_count=Coalesce(Count('user__article',distinct=True),0),
            article_likes=Coalesce(Count('user__articlelike',distinct=True),0),
            comment_count=Coalesce(Count('user__user_comments',distinct=True),0),
            comment_likes=Coalesce(Count('user__commentlike',distinct=True),0),
        )
        .annotate(
            total_score=(
                F('article_count')*3 +
                F('article_likes')*2 +
                F('comment_count')*1 +
                F('comment_likes')*2
            )
        )
        .order_by('-total_score')[:3]
    )
    
    
    return render(request,"about.html",{"top_authors":top_authors})

@login_required(login_url="user:login")
def dashboard(request):
    
    user=request.user
    
    profile = Profile.objects.get(user=user)
    
    
    articles=Article.objects.filter(author=user).order_by('created_date')
    
    article_count=articles.count() #makale sayısı
    
    article_likes=ArticleLike.objects.filter(article__author=user).count()
    #makalelerinin beğeni sayısı iki alt çizgi ile o tablonun ilgili ilişki kırmak
    #article üzerinden Article tarafına git Like değerini user a göre al pointer adresleme gibi
    
    comment_count=Comment.objects.filter(comment_author=user).count()
    #toplam yaptığı yorum sayısı
    
    comment_likes=CommentLike.objects.filter(comment__comment_author=user).count()
    #yorumların aldığı beğeni sayısı 
    
    paginator=Paginator(articles,4)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    context={
        "profile":profile,
        "articles":page_obj,
        "article_count":article_count,
        "article_likes":article_likes,
        "comment_count":comment_count,
        "comment_likes":comment_likes,
        "page_obj":page_obj,
    }
    
    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
@ratelimit(key='user', rate='3/m', block=True)
def addarticle(request):
    
    if getattr(request,'limits',False):
        
        return error_429_view(request)
    
    form=ArticleForms(request.POST or None,request.FILES or None)
    #makaelede resim de olabilir onun için sonradan ekleme request.FILES
    
    #form oluşturma ve gönderme
    
    if form.is_valid():#doğrulama kontrolü alanlar dolu mu
        article=form.save(commit=False)#modelle ilişkili olduğu için .save ile kaydedilir
        #eğer doğrudan kayderdersek yazar bilgisini alamdan yapar model
        #çünkü orada biz ekleyeceğiz diye vermemiştik
        #nenseyi oluşturup kaydetmeyi bizim yapmamız lazım
        article.author=request.user#yazara kullanıcıyı atama
        article.save()#şimdi kaydilebilir
        
        messages.success(request,"Makale Başarıyla Kaydedildi!.")
        
        return redirect("index")#kayıt başarılıysa yönlendirme
    
    return render(request,"addarticle.html",{"form": form})#post değilse gettir veya valid yanlışsa yönledirilir

def detail(request, id):
    # ID'ye göre makaleyi al, yoksa 404 döndür
    article = get_object_or_404(Article, id=id)
    
    # Ana yorumları al (sadece parent'ı olmayanlar)
    comments = article.comments.filter(parent__isnull=True)

    # Yazar profilini al
    author_profile = Profile.objects.get(user=article.author)
    
    # Makaledeki kelime sayısına göre okuma süresi hesapla
    plain_text = strip_tags(article.content)
    word_count = len(plain_text.split())
    reading_time = max(1, math.ceil(word_count / 200))  # En az 1 dakika

    # Kullanıcının bu makaleyi beğenip beğenmediğini kontrol et
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = ArticleLike.objects.filter(
            user=request.user,
            article=article
        ).exists()

        # Ana yorumlar ve alt yorumlar için beğeni durumunu ve sayısını ayarlama
        for comment in comments:
            comment.user_has_liked = comment.user_has_liked(request.user) if hasattr(comment, 'user_has_liked') else CommentLike.objects.filter(user=request.user, comment=comment).exists()
            comment.like_count = comment.like_count()

            # Alt yorumları (yanıtları) döngüyle işle
            for reply in comment.replies.all():
                reply.user_has_liked = reply.user_has_liked(request.user) if hasattr(reply, 'user_has_liked') else CommentLike.objects.filter(user=request.user, comment=reply).exists()
                reply.like_count = reply.like_count()
    else:
        # Giriş yapılmadıysa tüm beğeni durumu False
        for comment in comments:
            comment.user_has_liked = False
            comment.like_count = comment.like_count()

            for reply in comment.replies.all():
                reply.user_has_liked = False
                reply.like_count = reply.like_count()

    # Template'e gönderilecek veriler
    context = {
        'article': article,
        'comments': comments,
        'author_profile': author_profile,
        'reading_time': reading_time,
        'user_has_liked': user_has_liked,
    }
    
    return render(request, "detail.html", context)


@login_required(login_url="user:login") 
def updateArticle(request,id):
    
    article=get_object_or_404(Article,id=id)
    #id ye göre arayıp varsa makaleyi yoksa 404ü dönen taraf
    
    if article.author!=request.user:
        messages.warning(request,"Bu makaleyi düzenlemeye yetkiniz yok!!!")
        return redirect("article:dashboard")
    
    form=ArticleForms(request.POST or None, request.FILES or None,instance=article)
    #form nesnesi oluşturp içini veritabanından bilgilerle doldurma
    
    if form.is_valid():#makale doğruysa ve tamamsa gerisi addarticle ile aynı
        
        form.save()


        
        messages.success(request,"Makale Başarıyla Güncellendi!.")
        
        return redirect("index")#kayıt başarılıysa yönlendirme
    
    
    return render(request,"update.html",{"form":form,"article":article})

@login_required(login_url="user:login")
def deleteArticle(request,id):
    
    article=get_object_or_404(Article,id=id)#makaleyi alma
    
    article.delete()#silme
    
    messages.success(request,"Makale Silme Başarılı")
    
    return redirect("article:dashboard")


def articles(request):#makale sayfasında makaleleri gösteren yer
    
    keyword=request.GET.get("keyword")#aramadan gelen kelimeyi almak
    if keyword:#arama yapıldıysa gösterilecek get request yapılmadıysa ayrı get request gösterili
        
        articles=Article.objects.filter(title__contains=keyword)
        
        #sayfa başına makale gösterme için paginator modülü kullanılır
        paginator=Paginator(articles,6)#sayfa ve bölünecek elemanlar
        page_number=request.GET.get("page")#sayfa sayısı
        page_obj=paginator.get_page(page_number)#sayfa elemanları
        
        recent_posts=Article.objects.all().order_by('-created_date')[:5]
        #son içerikleri için son 5 makale atanması
        
        #veritabnından keyword içeren makaleleri alma
        return render(request,"articles.html",{
            "articles":page_obj,
            "page_obj":page_obj,
            "recent_posts":recent_posts,
            "keyword":keyword#arama sonuçları da sayfalansın
            
            })#gönderme
    
    #aksi durumda sadece tüm amkelelr görüntüelecenktir
    
    #tüm article ları sözlüğe alıp göstereceğiz 
    articles=Article.objects.all().order_by('created_date')#tüm makalelerin alınması
    
    paginator=Paginator(articles,6)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    
    recent_posts=Article.objects.all().order_by('created_date')[:5]
    
    return render(request,"articles.html",{
        "articles":page_obj,
        "page_obj":page_obj,
        "recent_posts":recent_posts
        
        })
    #html dosyasında sözlük oalrak gönderimi
    
@login_required
@ratelimit(key='user', rate='5/m', block=True)
def addComment(request,id):
    article=get_object_or_404(Article,id=id)#yorum yapılan makaleyi almak
    
    
    if getattr(request,'limits',False):
        return error_429_view(request)#sınır dışı istek atımında döndürülecek
    
    if request.method=="POST":#gelen metod kontrolü
        comment_author=request.POST.get("comment_author")#yazar bilgisi alınması
        comment_content=request.POST.get("comment_content")#yorum alınması
        parent_id=request.POST.get("parent_id")
        
        parent_comment=None
        
        if parent_id:
            try:
                parent_comment=Comment.objects.get(id=parent_id)
                #yorum objesinden parnet id atama
                
            except Comment.DoesNotExist:
                parent_comment=None
        
        newComment=Comment(comment_author=request.user,comment_content=comment_content,parent=parent_comment)
        #yorum dan nesne türetme
        
        newComment.article=article#yorumun makalesini atama
        
        newComment.save()#yorumu ekleme
        messages.success(request,"Yorumunuz Başarıyla Kaydedildi!")
    
    return redirect(reverse("article:detail",kwargs={"id":id}))#makalenin sayfasına yönlendirme
    #sayfa yorum yapılsa da yapılmasa da makalenin detay sayfasını göstereceği için gösterilir
    


#beğenme ve beğenmekten vazgeçme fonksiyonu


@login_required
@require_POST
def toggle_article_like(request, article_id):
    """
    Kullanıcı makaleyi beğenirse beğeni ekler, varsa kaldırır.
    Sonucu JSON olarak döner.
    """
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Makale bulunamadı."}, status=404)

    user = request.user
    existing_like = ArticleLike.objects.filter(user=user, article=article)

    if existing_like.exists():
        # Daha önce beğenmiş → kaldır
        existing_like.delete()
        liked = False
    else:
        # Beğeni ekle
        ArticleLike.objects.create(user=user, article=article)
        liked = True

    # En güncel beğeni sayısını tekrar hesapla
    like_count = ArticleLike.objects.filter(article=article).count()

    return JsonResponse({
        "liked": liked,
        "like_count": like_count
    })
    


#yorum beğenme fonksiyonu

@login_required
@require_POST

def toggle_comment_like(request, comment_id):
    
    #Kullanıcı yorumu beğenirse ekler tekrar beğenirse çeker
    
    try:
        comment=Comment.objects.get(id=comment_id)
    
    except Comment.DoesNotExist:
        
        return JsonResponse({"error":"Yorum Bulunamadı"},status=404)
    
    user=request.user
    existing_like=CommentLike.objects.filter(user=user, comment=comment)
    
    
    if existing_like.exists():
        
        #daha önce beğenmiştir kaldırma kısmı
        
        existing_like.delete()
        liked=False
        
    else:
        #Daha önce beğnememiştir ekle
        
        CommentLike.objects.create(user=user,comment=comment)
        liked=True
        
    like_count=CommentLike.objects.filter(comment=comment).count()
    #total beğeni sayısını alma
    
    return JsonResponse({
        
        "liked":liked,
        "like_count":like_count
    })
        