from django.contrib import admin
from django.urls import path
from . import views# fonksiyonların bulunduğu yeri import etme


app_name="article"

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('addarticle/',views.addarticle,name="addarticle"),
    path('article/<int:id>/',views.detail,name="detail"),
    path('update/<int:id>',views.updateArticle,name="update"),
    path('delete/<int:id>',views.deleteArticle,name="delete"),
    path('',views.articles,name="articles"),
    path('comment/<int:id>',views.addComment,name="comment"),
    path('like/<int:article_id>/',views.toggle_article_like, name="toggle_article_like"),
    path('comment-like/<int:comment_id>/',views.toggle_comment_like,name="toggle_comment_like"),
]