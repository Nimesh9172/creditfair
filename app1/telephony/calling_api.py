
import time
import json
import random, string
from ..models import *
from datetime import datetime
from app1.telephony.mqttclient import client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

token = "pkjyu"


def generate_request_id():
    request_id=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    request_id="CRDT"+request_id
    return request_id

def on_connect(client,usedata,flags,rc):
    if rc == 0:
        print("connected Successfully")
        global connected
        connected = True
        return
    else:
        print("connection failed")

# def connect():
#     return client

def publish(request):
    request_id=generate_request_id()
    if request.method == 'POST':
        phoneno = request.POST.get('number')[:10]
        current_datetime=datetime.now()
        extension = request.user.extension
        per_id=request.POST.get("per_id")
        t=datetime.now().time()
        t=t.strftime("%H:%M:%S")
        print("hhf ieuf",phoneno,extension,per_id)
        
        send_msg = { "cmd": "dial", "request_id": request_id,"callee": phoneno,"caller": extension}
        if AgentCall.objects.filter(extension=extension).exists() != True:
            AgentCall.objects.create(callee=phoneno,request_id=request_id,extension=extension)
        else:
            AgentCall.objects.filter(extension=extension).update(callee=phoneno,request_id=request_id,extension=extension)

        info = client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg),0,True)
        info.wait_for_publish()
        print(info.is_published())
        time.sleep(3)
        print(request_id)
        agentevents.objects.create(agentname=request.user.username,call_from=extension,call_to=phoneno,call_time=current_datetime,hang_time=current_datetime,disposed_time=current_datetime,personalkey_id=per_id)
        LeadDetails.objects.filter(id=per_id).update(AHT=t)

    return JsonResponse({'status':200})


def calling_response(request):
    if request.method == 'POST':
        print("post")
    q =  AgentCall.objects.filter(extension = request.user.extension)
    print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",q)
    return JsonResponse({'status':200,'response':list(q.values())}) 


def call_recording(request):
    send_msg={"cmd": "queue_paused","request_id": "e914b5997b762aa7","queue":"123456","extension":"8001",'paused':'no'}

    info = client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})




def call_conf(request):
    send_msg={"cmd": "conf_status","request_id": "27397bc2427c9274cb92","conf":"98675","dialpermission":"","member":"102"}

    info = client.publish(f"device/{token}/api/v1.0/command/conf",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})


def device_info(request):
    send_msg={"cmd": "deviceinfo","request_id": "27397bc2427c9274cb92"}
    info = client.publish(f"device/{token}/api/v1.0/command/system",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})


def hang_up(request):
    if request.method == 'POST':
        print("hanguppppppppppppppppppppppppppppppp")
        phoneno = request.POST.get('number')[:10]
        current_datetime=datetime.now()
        current_date = datetime.now().date()
        per_id=request.POST.get("per_id")
        extension=request.user.extension
        on_call=AgentCall.objects.filter(extension=extension).last()
        print(on_call.request_id,"parameters",on_call.callid,"***************************")
        send_msg={"cmd": "hangup","request_id":on_call.request_id, "callid": on_call.callid}
        info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
        info.wait_for_publish()
        print(info.is_published())
        time.sleep(3)
        agid = agentevents.objects.filter(call_time__icontains=current_date,personalkey=per_id,call_from=extension,call_to=phoneno).last()
        print(agid)
        if agid:
            agentevents.objects.filter(id=agid.id).update(hang_time=current_datetime,disposed_time=current_datetime,call_id=on_call.callid)
        return JsonResponse({'status':200})


def incoming_hangup(request):
    if request.method == 'POST':
        print("hangupgdgdgdgdgdgdgddg")
        request_id = generate_request_id()
        phoneno = request.POST.get('number')[:10]  
        per_id=request.POST.get("per_id")
        extension=request.user.extension
        current_datetime=datetime.now()
        current_date = datetime.now().date()
        on_call = Incoming_info.objects.filter(called=extension).last()
        AgentCall.objects.filter(extension=extension).update(callid=on_call.callid,callee=phoneno,event=on_call.direction)
        try:
            send_msg={"cmd": "hangup","request_id":request_id, "callid": on_call.callid}
            print(send_msg)
            info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
            info.wait_for_publish()
            print(info.is_published())
            time.sleep(3)
            agid = agentevents.objects.filter(call_time__icontains=current_date,personalkey=per_id,call_from=extension,call_to=phoneno).last()
            print('agid',agid)
            if agid:
                agentevents.objects.filter(id=agid.id).update(hang_time=current_datetime,disposed_time=current_datetime,call_id=on_call.callid)
            return JsonResponse({'status':200})

        except Exception as e:
            print(e)

        return JsonResponse({'status':200})
    

def incomming_response(request):
    if request.method == 'POST':
        phoneno = request.POST.get('number')[:10]
        current_datetime=datetime.now()
        extension = request.user.extension
        per_id=request.POST.get("per_id")
        print('phonenumber',phoneno)
        
        agentevents.objects.create(agentname=request.user.username,call_from=extension,call_to=phoneno,call_time=current_datetime,hang_time=current_datetime,disposed_time=current_datetime,personalkey_id=per_id)
        
    
    return JsonResponse({'status':200})


        

@csrf_exempt
def realtime(request):
    request_id = generate_request_id()
    print("its an request id",request_id)
    send_msg= {"cmd": "livecall", "request_id":request_id}
    info = client.publish(f"device/{token}/api/v1.0/command/system",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})



def ext_call_info_search(request):
   
    print("*******************************************************************")
    request_id = generate_request_id()
    ext=request.user.extension
    send_msg={"cmd": "extcallinfo","request_id": request_id,"extension":ext}
    info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published(),"piblishhhhhing")
    time.sleep(1)
    print("its calll")
    return JsonResponse({"status":200,"channelid" :"channelid"})


def attn_transfer(request):
    if request.method == "POST":
        to_num=request.POST.get("to_number")[:10]
        direction = request.POST.get('direction')
        peer=Calltransfer.objects.filter(to_num=request.user.extension).last()
        if direction == "outbound":
            peer=Calltransfer.objects.filter(extension=request.user.extension).last()
            
        Incoming_info.objects.filter(caller=peer.to_num).update(status="attend_transfer")
        request_id = generate_request_id()
        print(peer,"tooooooooooooooooooo",to_num)
        for i in to_num:
            print(i,to_num)
        send_msg={"cmd": "atxfer","request_id":request_id,"channelid":peer.channel_id,"tonumber":to_num}
        info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))

        info.wait_for_publish()
        print(info.is_published())
        time.sleep(3)
        return JsonResponse({"status":200})
    return JsonResponse({"status":300})


def attn_hangup(request):

    direction = request.POST.get('direction')
    print(direction,"directionsssssss")
    request_id = generate_request_id()
    peer=Calltransfer.objects.filter(to_num=request.user.extension).last()

    if direction == "outbound":
        peer=Calltransfer.objects.filter(extension=request.user.extension).last()

    
    send_msg={"cmd": "atxferoperate","request_id":request_id,"channelid":peer.channel_id,"operate":"complete"
}
    info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({"status":200})


def queue_paused(request):
    request_id = generate_request_id()
    print("itsss calll")
    extension=request.user.extension
    send_msg={"cmd": "queue_paused","request_id":request_id,"queue":"1023","extension":extension,"paused":"yes"}
    info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(2)
    return JsonResponse({"status":200})

def queue_unpaused(request):
    request_id = generate_request_id()
    extension=request.user.extension
    send_msg={"cmd": "queue_paused","request_id":request_id,"queue":"1023","extension":extension,"paused":"no"}
    info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({"status":200})



    