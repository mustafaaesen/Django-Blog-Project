from django.contrib import admin
from django.urls import path
from . import views# fonksiyonların bulunduğu yeri import etme

app_name="user"

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("contact/",views.contact,name="contact"),
]