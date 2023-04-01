from ..views_imports import *




def notificationCount(request):
    today = datetime.today()
    try:
        d4 = today.strftime("%Y-%m-%d")
        if request.user.user_level == 9:
            d=LeadDetails.objects.filter(callback_datetime__contains=d4).aggregate(total=Sum(Case(When( (Q(sub_disposition='Call Back')|Q(sub_disposition="Schedule Call")|Q(sub_disposition="Promise To Pay")),then=1),default=0
            )))
        else:
        
            d=LeadDetails.objects.filter(callback_datetime__contains=d4).filter(caller_name=request.user.username).aggregate(total=Sum(Case(When( (Q(sub_disposition='Call Back')|Q(sub_disposition="Schedule Call")|Q(sub_disposition="Promise To Pay")),then=1),default=0
            )))
            
        value=d["total"]
        print("reminder",value)
    except Exception as e:
        print(e)
  
    return JsonResponse({'value':value})


def misscallednotiCount(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    # d4="2022-09-22"
    if request.user.user_level == 9:
        d=Inbound_log.objects.filter(start__contains=d4,status="No").count()
        print("missssssssssssssssssssssssssssssssssssssssssssssss",d)
    else:
       
        d=Inbound_log.objects.filter(start__contains=d4,status="No").count()
        print(d)
        
    return JsonResponse({'d':d})


#///////////////// Recovery status filter Count starts///////////////////////
def recovery_count(request):
    if request.method == "POST":
        data=LeadDetails.objects
        if request.user.user_level != 9:
            data=data.filter(caller_name=request.user.username)
        
        data = data.exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)

        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
    
        print(fd , td,"dates")
        if fd != "" and td != "":
            fd = datetime.strptime(fd,'%d-%m-%Y')
            td = datetime.strptime(td,'%d-%m-%Y')
            if fd != td:
                td = td + timedelta(days=1)
            fd = fd.strftime("%Y-%m-%d")
            td = td.strftime("%Y-%m-%d")

        if fd == td:
            data = data.filter(contacted_dt__contains=td)
        else:
            data = data.filter(contacted_dt__range=[fd,td])


        print(data,"ASDASDADASDADPAPPDAPDDPAAPADPAPAPD")

    cn = data.values("sub_disposition").order_by("sub_disposition").annotate(the_count=Count("sub_disposition"))
    print(type(cn),cn,"recovery count")

    return JsonResponse({"status":200,"data":list(cn)})

#///////////////// Recovery status filter Count ends///////////////////////
