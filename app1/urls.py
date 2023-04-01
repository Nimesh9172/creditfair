from . import views
from django.conf import settings
from django.urls import path
from .telephony.subscriber_api import *
from django.conf.urls.static import static
from .utils.cms import *
from .utils.leadupdate import *
from .utils.dndupdate import *
from .utils.createuser import *
from .utils.apr_views import *
from .utils.login_logout import *
from .utils.dashboard import *
from .telephony import calling_api
from app1 import export_views
from .utils.upload_export import *
from .utils.incomming import *
from .utils.search import search,searchajax
from .utils.notification import recovery_count,notificationCount,misscallednotiCount
from .utils.misscalled import missajax,check_missedcall
from .utils.callmanagement import filterrm,filterrs
from .utils.qualityscore import qsajax,scoredata,score,qsexport
from .utils.teamoverall import ptpajax,ptpcount,paidcount,tvajax

urlpatterns = [
    path('',views.home,name="home"),

    path('login',loginuser,name="login"),
    path('login_user_ajax',login_user_ajax,name="login_user_ajax"),
    path('logout',logoutuser,name="logout"),

    path('search/',search, name='search'),
    path('sajax',searchajax,name="sajax"),

    path('cms',cms,name="cms"),
    path('cms_submit_ajax',cms_submit_ajax,name="cms_submit_ajax"),
    path('addition_details_ajax',addition_details_ajax,name="addition_details_ajax"),
    path('get_additional_info',get_additional_info,name="get_additional_info"),
    path('get_additional_numbers',get_additional_numbers,name="get_additional_numbers"),
    path('customer_history',customer_history,name="customer_history"),

    path('inc_cms',inc_cms,name="inc_cms"),
    path('updatefield',updatefield,name="updatefield"),
    path('incoming_search_ajax',incoming_search_ajax,name="incoming_search_ajax"),
    path('card1update',card1update,name='card1update'),

    path("check_for_incoming",check_for_incoming,name="check_for_incoming"),

    path("rt",calling_api.realtime,name="rt"),
    path("incomming_response",calling_api.incomming_response,name="incomming_response"),
    path("incoming_hangup",calling_api.incoming_hangup,name="incoming_hangup"),
    path("queue_paused",calling_api.queue_paused,name="queue_paused"),
    path("queue_unpaused",calling_api.queue_unpaused,name="queue_unpaused"),


    path('reminder',views.reminder,name="reminder"),

    path('recovery',views.recovery,name="recovery"),

    path('missedcall',views.missedcall,name="missedcall"),

    path('ots',views.ots,name="ots"),

    path('non_attempted',views.non_attempted,name="non_attempted"),

    path('connect_to_customer',views.connect_to_customer,name="connect_to_customer"),

    path('upload_export',upload_export,name="upload_export"),
    path('dataexport',dataexport,name="dataexport"),
    path('upload_ajax',upload_ajax,name="upload_ajax"),
    path('check_list_id',check_list_id,name="check_list_id"),
    path("datastatus/",datastatus,name="datastatus"),

    path('creatuser',createuser,name="creatuser"),
    path('save',savedata,name='save'),
    path('delete/',deletepost,name='deletepost'),
    path('updateuser/',updateuser,name="updateuser"),
    path('searchintable/',search_in_table,name='search'),

    path('leadupdate',leadupdate,name="leadupdate"),
    path('check_list_id_leadupdate',check_list_id_leadupdate,name="check_list_id_leadupdate"),
    path('uploadajax_lead',uploadajax_lead,name="uploadajax_lead"),
    
    path('dnd',dnd_view,name="dnd"),
    path('uploadajax_dnd',uploadajax_dnd,name="uploadajax_dnd"),

    path('sms',views.sms,name="sms"),

    path('get_dispositions',views.get_dispositions,name="get_dispositions"),


    path('dashboard',views.home,name="dashboard"),

    
    #///////////////////Call management starts////////////////////
    path("filterrm",filterrm,name="filterrm"),
    path("filterrs",filterrs,name="filterrs"),
    path("recovery_count",recovery_count,name="recovery_count"),
    #///////////////////Call management ends////////////////////

    #Teamoverall
    path('lead_behaviour',views.lead_behaviour,name="lead_behaviour"),
    path('ptp_status',views.ptp_status,name="ptp_status"),
    path('paid_status',views.paid_status,name="paid_status"),
    path('dispo_status',views.dispo_status,name="dispo_status"),

    path("ptpajax",ptpajax,name="ptpajax"),
    path("ptpcount",ptpcount,name="ptpcount"),
    path("paidcount",paidcount,name="paidcount"),
    path("tvajax",tvajax,name="tvajax"),

    #/////////////////Miss Call starts///////////////////
    path("missajax",missajax,name="missajax"),
    path("check_missedcall",check_missedcall,name="check_missedcall"),

    #////////////////Miss Call ends//////////////////////

    # //////////////Notification starts/////////////////////
    path("notificationCount",notificationCount,name="notificationCount"),
    path("misscallednotiCount",misscallednotiCount,name="misscallednotiCount"),
    # /////////////Notification Ends//////////////////////



    # quality
    path("quality",views.quality,name="quality"),
    path("qsajax",qsajax,name="qsajax"),
    path('scoredata',scoredata,name='scoredata'),
    path("score_card/<int:id>",views.score_card,name="score_card"),
    path('score',score,name="score"),
    path("qualityexport",views.qualityexport,name="qualityexport"),
    path("qsexport",qsexport,name="qsexport"),

     # urls for subscriber_api.py 
    path("check_misscall",check_misscall,name="check_misscall"),
    path("update_status",update_status,name="upate_status"),
    path("create_cdr",create_cdr,name="create_cdr"),
    path("update_calltransfer",update_calltransfer,name="update_calltransfer"),
    path("insert_incoming",insert_incoming,name="insert_incoming"),
    path("delete_incoming",delete_incoming,name="delete_incoming"),
    # urls for subscriber_api.py ends

    
    #Dashboard
    path('dashboard/',views.home,name="dashboard"),
    path("total_calls",total_calls,name="total_calls"),
    path("agent_available",agent_available,name="agent_available"),
    path("top_five_dispo",top_five_dispo,name="top_five_dispo"),
    path("paid_ptp_status",paid_ptp_status,name="paid_ptp_status"),
    path("call_status",call_status,name="call_status"),


    
    #////////////////Data Export for every pages starts//////////////
    path('exportrm',export_views.export_reminder,name="exportrm"),
    path('export_recovery',export_views.export_recovery,name="export_recovery"),
    path('exportmiss',export_views.export_misscall,name="exportmiss"),
    path("export_qualityscore",export_views.export_qualityscore,name="export_qualityscore"),
    #////////////////Data Export for every pages ends//////////////

       # ////////////mqttt links start////////////
    path('publish',calling_api.publish,name="publish"),
    path('call_response',calling_api.calling_response,name="call_response"),
    path('queue',calling_api.call_recording,name="queue"),
    path('conf',calling_api.call_conf,name="conf"),
    path('info',calling_api.device_info,name="info"),
    path("hangup",calling_api.hang_up,name="hangup"),
    path("incomming_response",calling_api.incomming_response,name="incomming_response"),
    # ////////////mqttt links end////////////

     # ////////////new apr linksss start 8/1/2023 ///////////
    path("apr_test",test,name="apr_test"),
    path("call_apr",call_apr,name="call_apr"),
    path("hangup_apr",hangup_apr,name="hangup_apr"),
    path("dispose_apr",dispose_apr,name="dispose_apr"),
    path("login_apr",login_apr,name="login_apr"),
    path("logout_apr",logout_apr,name="logout_apr"),
    path("apr_report_export",apr_report_export,name="apr_report_export"),
    path('break_events',break_events,name="break_events"),
    # ////////////new apr linksss end 8/1/2023 ///////////

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


