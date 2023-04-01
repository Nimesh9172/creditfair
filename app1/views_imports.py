from django.shortcuts import render,redirect
from datetime import datetime,timedelta,time,date
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count,Sum,Case,When,F,Q
from .serializers import *
# from .apr_views import *
import pandas as pd
import xlwt
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



def cdr_update_dispositions(subval,ext,username,id):
    print("crd update called",subval,ext,username,id)
    t=datetime.now().time().strftime("%H:%M:%S")

    try:

        on_call=AgentCall.objects.filter(extension=ext).last()
        print("Oncalllllllll",on_call)
        cdr_a=CallRecording.objects.filter(callid=on_call.callid).last()
        print("????????Cdr",cdr_a)
        CallRecording.objects.filter(id=cdr_a.id).update(agentname=username,sub_dispos=subval)
        prev=LeadDetails.objects.filter(id=id).last()
        if prev :
            format="H%:%M:%S"
            p=prev.AHT
            p_t=datetime.strptime(p, "%H:%M:%S")
            t_t=datetime.strptime(t, "%H:%M:%S")
            print(t,type(t),type(prev.AHT),prev.AHT,type(p_t),type(t_t))
            time_difference =  t_t-p_t
            # calc=t-prev.AHT
            print(LeadDetails.objects.filter(id=id),"objjjjjjjjjjjjj")
            LeadDetails.objects.filter(id=id).update(AHT=time_difference)
            obj = LogData.objects.filter(lead_forkey=id).last()
            LogData.objects.filter(id=obj.id).update(AHT=time_difference)
            print(time_difference,"itsssssssssssssssssssssss")
    except Exception as e:
        print(e)

    return JsonResponse({"status":200})



