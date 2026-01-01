from django import forms

from .models import Article

#daha önce formlardan nesne türetirken şimdi makale için
#modelformdan türetebliriz
#models.py içerisinden import edip metasını değiştirerek kullanılır

class ArticleForms(forms.ModelForm):
    
    class Meta:
        
        model=Article
        #models.py de author ve created alanlarını istemiyoruz bu biglileri biz alacağız elimizde var
        #başlık ve içerik alanı oluşturmalı
        
        fields=["title","interest_area","content","article_image"]
        
        widgets={
            
            "title":forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Makale Başlığı Giriniz'
            }),
            
            "interest_area":forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Makalenin İlgi Alanını Giriniz(Ör.Yapay Zeka)'
            }),
            
            "content":forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Makalenizi Buraya Yazmaya Başlayın...',
                'rows':8
            }),
            "article_image":forms.ClearableFileInput(attrs={
                'class':'form-control',
            })
            
            
        }
        
        labels={
            "title":"Makale Başlığı",
            "interest_area":"İlgi Alanı",
            "content":"Makale İçeriği",
            "article_image":"Makale Görseli",
        }
        