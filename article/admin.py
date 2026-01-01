from django.contrib import admin

# Register your models here.

from.models import Article,Comment#modeldeki article modelinin importu

#admin.site.register(Article)#modelin gösterimi
#import edilen class burada decorator ile özelleştirilerek farklı format kazandırılır

admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Article modeline özel admin görünümü
    
    list_display = ["title", "author", "interest_area", "created_date"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title", "interest_area"]
    list_filter = ["created_date", "interest_area"]

    class Meta:
        model = Article
        
    