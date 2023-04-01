from ..models import *
from datetime import datetime,timedelta
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum,Case,When,F,QuerySet,Q
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def update_status(request):
    print('its post not')
    if request.method == "POST":
        print("in post")
        extension = request.POST.get("extension")
        status = request.POST.get("status")
        message = request.POST.get("message")
        callid = request.POST.get("callid")
        request_id = request.POST.get("request_id")
        # AgentCall.objects.filter(extension=extension).update(status=status)
        print("from update status function",extension,status,message,callid)
        if request_id :
            AgentCall.objects.filter(request_id=request_id).update(callid=callid)
        else:
            AgentCall.objects.filter(extension=extension).update(status=status)        
    return JsonResponse({'status':200})

@csrf_exempt
def create_cdr(request):
    print("in create cdr")
    if request.method=="POST":
        callid=request.POST.get('callid')
        src=request.POST.get("src")
        srctech=request.POST.get("srctech")
        dst=request.POST.get("dst")
        dsttech=request.POST.get("dsttech")
        start=request.POST.get("start")
        end=request.POST.get("end")
        billsec=request.POST.get("billsec")
        disposition=request.POST.get("disposition")
        direction=request.POST.get("direction")
        recordfile=request.POST.get("recordfile")
        CallRecording.objects.create(callid=callid,src=src,srctech=srctech,dst=dst,dsttech=dsttech,start=start,end=end,billsec=billsec,disposition=disposition,direction=direction,recordfile=recordfile)
    return JsonResponse({'status':200})

@csrf_exempt
def update_calltransfer(request):
    dt=datetime.now()
    if request.method == "POST":
        ext=request.POST.get('ext')
        callid=request.POST.get('callid')
        peer_id=request.POST.get('peer_id')
        channelid=request.POST.get('channelid')
        direction=request.POST.get('direction')
        to=request.POST.get('to')
        res=Calltransfer.objects.filter(extension=ext).last()
        if not res:
            Calltransfer.objects.create(extension=ext,call_id=callid,peer_id=peer_id,channel_id=channelid,direction=direction,to_num=to)
        else:
            Calltransfer.objects.filter(extension=ext).update(call_id=callid,peer_id=peer_id,channel_id=channelid,direction=direction,to_num=to)
    return JsonResponse({'status':200})


@csrf_exempt
def insert_incoming(request):
    if request.method=="POST":
        ext=request.POST.get("ext")
        direction=request.POST.get("direction")
        source=request.POST.get("source")
        destination=request.POST.get("destination")
        callid=request.POST.get("callid")
        called=request.POST.get("called")
        income_date=request.POST.get("income_date")
        status=request.POST.get("status")
        res=Incoming_info.objects.filter(caller=ext).last()
        if not res:
            res=Incoming_info.objects.create(caller=ext,direction=direction,source=source,destination=destination,callid=callid,called=called,income_date=income_date,status=status)
    return JsonResponse({'status':200})


@csrf_exempt
def delete_incoming(request):
    if request.method == 'POST':
        numbers_str=request.POST.get('numbers_str')
        
        if len(numbers_str) > 3:
            numbers_str=numbers_str.split(',')
        else:
            print(numbers_str,"aljsdkaklsjdaklsjdasjdaslk")
        print('fromm delete',numbers_str,type(numbers_str))
        Incoming_info.objects.exclude(caller__in=numbers_str).delete()
    return JsonResponse({'status':200})


@csrf_exempt
def check_misscall(request):
    if request.method == "POST":
        mobile_number=request.POST.get("src")
        callid=request.POST.get("callid")
        srctech=request.POST.get("srctech")
        dst=request.POST.get("dst")
        dsttech=request.POST.get("dsttech")
        start=request.POST.get("start")
        end=request.POST.get("end")
        billsec=request.POST.get("billsec")
        disposition=request.POST.get("disposition")
        direction=request.POST.get("direction")
        recordfile=request.POST.get("recordfile")
        try:
            print(mobile_number,callid,srctech,dst,start,end,billsec,disposition,direction,recordfile,"all parameters")
            
            d=datetime.now().date()

            check=Inbound_log.objects.filter(src__icontains=mobile_number,start__icontains=d,status="No").last()
            if check:
                Inbound_log.objects.filter(id=check.id).update(count=F("count")+1)
            else:
                print("ready to create")
                Inbound_log.objects.create(src=mobile_number,callid=callid,srctech=srctech,dsttech=dsttech,dst=dst,start=start,end=end,billsec=billsec,disposition=disposition,direction=direction,recordfile=recordfile,status="No",count=1)
        except Exception as e:
            print(e)

    return JsonResponse({"status":200})

