from django.shortcuts import render

# Create your views here.

def render_error_page(request,code,title,description):
    
    context={
        "code":code,
        "title":title,
        "description":description
    }
    
    return render(request,"errors.html",context,status=code)


def error_404_view(request, exception=None):
    
    return render_error_page(request,404,"Oops!Sayfa Bulunamadı","Aradığınız sayfa mevcut değil veya kaldırılmış olabilir")

def error_403_view(request, exception=None):
    
    return render_error_page(request,403,"Oops!Erişim Engellendi","Bu işlemi yapmak için gerekli izniniz yok")

def error_405_view(request):
    
    return render_error_page(request,405,"Oops!Geçersiz İstek","Bu sayfaya gönderilen istek türü desteklenmiyor")

def error_429_view(request):
    
    return render_error_page(request,429,"Oops!Çok Fazla İstek","Lütden bekledikten sonra tekrar deneyiniz")

def error_500_view(request):
    
    return render_error_page(request,500,"Oops!Sunucu Hatası","Bir hata oluştu.Lütfen daha sonra tekrar deneyiniz")