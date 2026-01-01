from django.db import models

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Article(models.Model):
    #user tablosundan makale içeriğini türetme türüdür.
    
    author=models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Yazar")
    #yazar user tablosundan türetildi ve on delete ile kullanıcı silinirse içerikleri de silinecek
    #şekilde ayarlandı
    
    title=models.CharField(max_length=50,verbose_name="Başlık")#başlık ayarlandı max 50 uzunlukta
    
    interest_area = models.CharField(max_length=100, blank=True, null=True, verbose_name="İlgi Alanı")

    
    content=RichTextField(verbose_name="İçerik") #içerik
    
    
    created_date=models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")#oluşturulma tarihi veritabnına eklendiği tarih
    #verbose name ile balık alanları türkçelerştirildi
    
    #article object ve numarası yerine makale başlığının yazılması
    
    article_image = models.FileField( upload_to='article_pics/' ,default='article_pics/default_article.jpg',blank=True, null=True, verbose_name="Makalenin Fotoğrafı")

    #makalenin görsel oladabilir olmayabilir alanın ayrılması
    
    def __str__(self):
        return self.title    #makale başlığı listelenir

    class Meta:
        ordering=["created_date"]
        
    
    def save(self,*args,**kwargs):
        
        if not self.article_image or self.article_image.name == "":#kullanıcı olan resmi silmişse ve yerine resim eklememişsse defaulta düş
            self.article_image="article_pics/default_article.jpg"
        
        super().save(*args,**kwargs)
        
    def like_count(self):
        
        return self.likes.count()#beğeni sayısını döner geri
    
    def user_has_liked(self,user):
        
        #kullanıcı bu makaleyi beğenmiş mi kontrolü yapar
        
        return self.likes.filter(user=user).exists()

class Comment(models.Model):
    
    article=models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Makale",related_name="comments")
    #bir makalenin birden fazla yorumu olabilir foreign key ile ilişki atandı
    #makale silinirse yorum da silinsin diye on_delete mevcut
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment_content=models.CharField(max_length=250,verbose_name="Yorum")
    #yorum metni
    comment_date=models.DateTimeField(auto_now_add=True)
    #yorum tarihi otomatik eklemek için
    
    parent=models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    #yanıt verilen yorumlar için parent ilişkisi kuruldu yorumun parenti varsa o yoru yanıttır ilgili yerde gösteirlir
     
    def __str__(self):
        return self.comment_content
    
    
    class Meta:
        ordering=["-comment_date"]
        
    def like_count(self):
        return self.commentlike_set.count()
    
    def user_has_liked(self, user):
        """Kullanıcı bu yorumu beğenmiş mi kontrol eder."""
        return self.commentlike_set.filter(user=user).exists()

#makale beğenme modeli

class ArticleLike(models.Model):
    
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    #beğenen kullanıcnın bilgilerini atama foregin key ile ilişki
    article=models.ForeignKey('Article', on_delete=models.CASCADE, related_name='likes')
    #beğenilen makale bilgilerinin atama foreign key ile
    
    created_at=models.DateTimeField(auto_now_add=True)
    #beğenme zamanı
    
    class Meta:
        
        unique_together= ('user','article')
        #birlikte özlük atama bir kullanıcı bir makaleyi bir kez beğenebilir
        #ikinci kez tıklarsa beğeni çeker
        
    
    def __str__(self):
        
        return f"{self.user.username} beğendi {self.article.title}"
    
    #ARTICLE modeline makalenin beğeni sayısını veren ve kulalnıcnın makaleyi beğendiğini
    #gösteren metodları da ekle  def like_count def user_has_liked
    
    
    

#Yorum Beğenme

class CommentLike(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #beğenen kullanıcı bilgileri için ilişki kurulması
    comment=models.ForeignKey("Comment", on_delete=models.CASCADE)
    #beğenilen yorum ilişki atanması
    #oluşup oluşmamalarına bağlı olarak tırnak içlerinde yazılır article da comment da kendi modelelrinin
    #altındalarsa gereksizdir ama ne olur ne olmaz string veri göndermek gerekebilirz
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        
        unique_together=('user','comment')
        #aynı kullanıcı aynı yorumu bir kez ebeğenibilir 
        
    def __str__(self):
        
        return f"{self.user.username} liked comment {self.comment.id}"