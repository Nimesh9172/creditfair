from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.home,name="home"),

    path('login',views.loginuser,name="login"),
    path('login_user_ajax',views.login_user_ajax,name="login_user_ajax"),
    path('logout',views.logoutuser,name="logout"),

    path('search', views.search, name='search'),
    path('sajax',views.searchajax,name="sajax"),

    path('reminder',views.reminder,name="reminder"),

    path('recovery',views.recovery,name="recovery"),

    path('missedcall',views.missedcall,name="missedcall"),

    path('ots',views.ots,name="ots"),

    path('non_attempted',views.non_attempted,name="non_attempted"),

    path('connect_to_customer',views.connect_to_customer,name="connect_to_customer"),

    path('upload_export',views.upload_export,name="upload_export"),

    path('leadupdate',views.leadupdate,name="leadupdate"),
    
    path('dnd',views.dnd,name="dnd"),

    path('sms',views.sms,name="sms"),


    path('dashboard',views.home,name="dashboard"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


