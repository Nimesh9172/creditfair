from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from .utils.upload_export import check_list_id,upload_ajax,upload_export,datastatus
from .utils.search import search,searchajax

urlpatterns = [
    path('',views.home,name="home"),

    path('login',views.loginuser,name="login"),
    path('login_user_ajax',views.login_user_ajax,name="login_user_ajax"),
    path('logout',views.logoutuser,name="logout"),

    path('search',search, name='search'),
    path('sajax',searchajax,name="sajax"),

    path('reminder',views.reminder,name="reminder"),

    path('recovery',views.recovery,name="recovery"),

    path('missedcall',views.missedcall,name="missedcall"),

    path('ots',views.ots,name="ots"),

    path('non_attempted',views.non_attempted,name="non_attempted"),

    path('connect_to_customer',views.connect_to_customer,name="connect_to_customer"),

    path('upload_export',upload_export,name="upload_export"),
    path('upload_ajax',upload_ajax,name="upload_ajax"),
    path('check_list_id',check_list_id,name="check_list_id"),
    path("datastatus/",datastatus,name="datastatus"),


    path('leadupdate',views.leadupdate,name="leadupdate"),
    
    path('dnd',views.dnd,name="dnd"),

    path('sms',views.sms,name="sms"),


    path('dashboard',views.home,name="dashboard"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


