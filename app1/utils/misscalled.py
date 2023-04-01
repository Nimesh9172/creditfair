from ..views_imports import *

# /////////////////////////Missedcall function starts/////////////////////////

def missajax(request):
    miss=Inbound_log.objects
    if request.method=="POST":
        miss=Inbound_log.objects.all()
        filt = request.POST.get("filter")
        sd=request.POST.get("sd").rstrip()
        ed=request.POST.get("ed").rstrip()
        sd=datetime.strptime(sd,'%d-%m-%Y')
        ed=datetime.strptime(ed,'%d-%m-%Y')

        sd=sd.strftime("%Y-%m-%d")
        ed=ed.strftime("%Y-%m-%d")
        print("missssssssscalllssssss",miss)
        if request.user.user_level == 9: 
            miss=Inbound_log.objects.filter(start__range=[sd,ed])
            if sd == ed:
               miss=Inbound_log.objects.filter(start__contains=ed)
               print(miss,"date starts")
        else:
            miss=Inbound_log.objects.filter(start__range=[sd,ed])
            if sd == ed:
               miss=Inbound_log.objects.filter(start__contains=ed)

        
        

        if filt == "all":
            miss = miss.filter(status__isnull = False)
        elif filt == "completed":
            miss = miss.filter(status = "Yes")
        elif filt == "no":
            miss = miss.filter(status = "No")
        elif filt == "rnr":
            miss = miss.filter(status = "Ringing No Response")

        miss = miss[:150]
        
        return JsonResponse({"miss":list(miss.values())})
    return JsonResponse({"status":600})



def check_missedcall(request):
    ph=request.GET.get("phone")
    print("check missed",ph)
    ph=ph[-10:]
    print(ph,"phhhhhhhh")
    try:
        add=AdditionalInfo.objects.values_list('lead_id',flat=True).filter(phone_no=ph).last()
        print(add,"asdasd")

        per=LeadDetails.objects.filter(Q(id = add) |Q(mobile_no=ph)|Q(additional_no=ph)).last()
        if per:
            per=per.id
            print("iffffffffffffffffffffffffffffff ",per)   
        else:
            per=LeadDetails.objects.create(mobile_no=ph,created_by="MissedCall")
            per.save()
            per = per.id
            print("in elseeeeeeeeeeeeeeeeeeeeeeeeeee",per)
        
        return JsonResponse({"status":200,"id":per,"ph":ph})

    except Exception as e:
        print(e,"error")
    
        return JsonResponse({"status":200,"id":per,"ph":ph})

    



# //////////////////Missedcall function  ends//////////////
