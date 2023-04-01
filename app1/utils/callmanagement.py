from ..views_imports import *

def filterrm(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    if request.user.user_level == 9:
       data=LeadDetails.objects.filter(Q(sub_disposition="Promise To Pay")|Q(sub_disposition="Call Back")|Q(sub_disposition="Schedule Call"))
       print("in 9",data)

       all_ct=data.count()
       ptp_ct=LeadDetails.objects.filter(sub_disposition="Promise To Pay")
       cbk_ct=LeadDetails.objects.filter(sub_disposition="Call Back")
       scbk_ct=LeadDetails.objects.filter(sub_disposition="Schedule Call")
    
    else:
        data=LeadDetails.objects.filter(caller_name=request.user.username).filter(Q(sub_disposition="Promise To Pay")|Q(sub_disposition="Call Back")|Q(sub_disposition="Schedule Call"))
        print("in else",data)
        all_ct=data.count()
        ptp_ct=LeadDetails.objects.filter(caller_name=request.user.username).filter(sub_disposition="Promise To Pay")
        cbk_ct=LeadDetails.objects.filter(caller_name=request.user.username).filter(sub_disposition="Call Back")
        scbk_ct=LeadDetails.objects.filter(caller_name=request.user.username).filter(sub_disposition="Schedule Call")
    
    
    if request.method == "POST":
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
        fil = request.POST.get('remfilter')
        fil = fil.split(",")
        sortval = request.POST.get('sortby') 
        print("filll",fil,sortval)
        try:

            if fd != "" and td != "":
                fd = datetime.strptime(fd,'%d-%m-%Y')
                td = datetime.strptime(td,'%d-%m-%Y')
                if fd != td:
                    td = td + timedelta(days=1)
                    
                fd = fd.strftime("%Y-%m-%d")
                td = td.strftime("%Y-%m-%d")

                if fd == td:
                    data = data.filter(callback_datetime__icontains=fd)
                    all_ct=data.filter(callback_datetime__icontains=fd).count()
                    ptp_ct=data.filter(sub_disposition='Promise To Pay').count()
                    cbk_ct=data.filter(sub_disposition='Call Back').count()
                    scbk_ct=data.filter(sub_disposition='Schedule Call').count()
                    
                else:
                    print("adadaaad",td,fd)
                    
                    data = data.filter(callback_datetime__range=[fd,td])
                    all_ct = data.filter(callback_datetime__range=[fd,td]).count()

                    ptp_ct=data.filter(sub_disposition='Promise To Pay').count()
                    cbk_ct=data.filter(sub_disposition='Call Back').count()
                    scbk_ct=data.filter(sub_disposition='Schedule Call').count()
                    print("inssisiisisisis",data)
            
           
            if sortval != '':
                print("SORT",sortval)
                if sortval == "ascending":
                    data = data.order_by('amount')
                    print(data,"sortval")
                elif sortval == "descending":
                    data = data.order_by('-amount')  
                    print(data,'itstsjs')  
            if fil != ['']:
                data = data.filter(Q(sub_disposition__in=fil))
        
        except  Exception as e:
            print(e)
            
    print("all_data",all_ct,ptp_ct,cbk_ct,scbk_ct)
    return JsonResponse({'data':list(data.values()),"all_ct":all_ct,'ptp_ct':ptp_ct,"cbk_ct":cbk_ct,"scbk_ct":scbk_ct})


def filterrs(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    data=LeadDetails.objects
    if request.user.user_level == 9:
        data=LeadDetails.objects.exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)
    else:
        data=LeadDetails.objects.filter(caller_name=request.user.username).exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)

    if request.method == "POST":
        
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
        sel = request.POST.get('sortval')
        print(td,"tdddd")
        sel = sel.split(",")
        try:
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
                
          
            if sel != ['']:
            
                data = data.filter(Q(sub_disposition__in=sel))
                
            print("asdsaaaaaddda",data)

        except Exception as e:
            print(e)
    return JsonResponse({'data':list(data.values())})

