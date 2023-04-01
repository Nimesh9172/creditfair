from ..views_imports import *


def ptpajax(request):
    if request.method=="POST":
        agent=request.POST.get("ptpagent")
        bk=request.POST.get('bankname')
        
        print("detaiiiiiils",agent,"bankkkkkkkkk",bk)
        if request.user.user_level==9:
            data =  ptpbehaviour.objects.exclude(next_status="Paid")
            print("dataaa9",data)
        else:
            data = ptpbehaviour.objects.filter(callerid=request.user.username).exclude(next_status="Paid")
            print("dataaa1",data)

        if agent !="" and agent !="all":
            data = data.filter(callerid=agent)
            print("aagenttt",data)
        
        elif agent =="all":
             data =  ptpbehaviour.objects.exclude(next_status="Paid")
            
        if bk !="" and bk!="all":
            data = data.filter(lender_name=bk).exclude(next_status="Paid")
            print("dataaabk",data)
        
        elif bk =="all" :
             data = data.filter(lender_name__isnull=False)
            

        return JsonResponse({"b":list(data.values())})
    return JsonResponse({'log_data':200})

    

def ptpcount(request):

    agent=User.objects.all()
    ls=[]
    usl=[]
    twl=[]
    tml=[]
    tosl=[]
    ptpl=[]
    ptpper=[]
    # d={}
    today=datetime.now().date()
    this_week = today + timedelta(days=7)
    this_month=  today + timedelta(days=30)
    print(this_week,"next",this_month)
    for i in agent:
        if request.user.user_level == 1:
            i.username=request.user.username
            print(i.username)
        us=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Promise To Pay").filter(callback_datetime__icontains=today).count()
        tw=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Promise To Pay").filter(callback_datetime__range=[today,this_week]).count()
        tm=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Promise To Pay").filter(callback_datetime__range=[today,this_month]).count()
        main=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Promise To Pay").filter(callback_datetime__range=[today,this_month]).aggregate(Sum('main_amount'))
        t=main['main_amount__sum']
        ptp=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Promise To Pay").filter(callback_datetime__range=[today,this_month]).aggregate(Sum('amount'))
        print(ptp,"pppppppppppppppppppppppppppppppppppppppp")
        a=ptp['amount__sum']
        # print("asls",tos['TOS__sum'])
        try: 
            if a != None:
                per=round((a/t)*100,2)
                ptpper.append(per)
            else:
                per=0
                
                ptpper.append(per)
        except Exception as e:
                print(e)

        usl.append(us)
        twl.append(tw)
        tml.append(tm)
        tosl.append(t)
        ptpl.append(a)
        # print(i.username,us,tw,tm)
        ls.append(i.username)
        # d[ls[i.username]]=values[us]
   
        d={i:{} for i in ls}
        count=0
        try :
            for i in d:
                if len(d) !=0:
                    d[i] = {'td':usl[count],"tw":twl[count],"tm":tml[count],"tos":tosl[count],"ptp":ptpl[count],"per":ptpper[count]}
                    count+=1
                else:
                    d[i] = {'td':usl[count],"tw":twl[count],"tm":tml[count],"tos":tosl[count],"ptp":ptpl[count],"per":ptpper[count]}
        except Exception as e:
            print(e)

    ptp=LeadDetails.objects.filter(caller_name__in=ls).filter(sub_disposition="Promise To Pay")
    print(d)
    print("this",ptpper)
    for i in ptp:
        pass
    #     print(i.callername)
    # print(ptp)
    
    print(today)
    return JsonResponse({"d":d})

def paidcount(request):
    
    agent=User.objects.all()
    ls=[]
    usl=[]
    twl=[]
    tml=[]
    tosl=[]
    paidl=[]
    paidontos=[]
    # d={}
    today=datetime.now().date()
    this_week = today + timedelta(days=7)
    this_month=  today + timedelta(days=30)
    print(this_week,"next",this_month)

    

    for i in agent:
        if request.user.user_level == 1:
            i.username=request.user.username
            print(i.username)
        us=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Paid").filter(contacted_dt__icontains=today).count()
        tw=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Paid").filter(contacted_dt__range=[today,this_week]).count()
        tm=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Paid").filter(contacted_dt__range=[today,this_month]).count()
        main=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Paid").filter(contacted_dt__range=[today,this_month]).aggregate(Sum('main_amount'))
        t=main['main_amount__sum']
        paid=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Paid").filter(contacted_dt__range=[today,this_month]).aggregate(Sum('cash'))
        p=paid['cash__sum']
        print("asls",p,type(p))
        if p != None:
            percent=round((p/t)*100,2)
            paidontos.append(percent)
            
        else:
            percent="0"
            paidontos.append(percent)


        usl.append(us)
        twl.append(tw)
        tml.append(tm)
        tosl.append(t)
        paidl.append(p)
        # print(i.username,us,tw,tm)
        ls.append(i.username)
        # d[ls[i.username]]=values[us]

    d={i:{} for i in ls}
    count=0
   
    try :
        for i in d:
            if len(d)!=0:
            
                d[i] = {'td':usl[count],"tw":twl[count],"tm":tml[count],"tos":tosl[count],"ptp":paidl[count],"paidontos":paidontos[count]}
                count+=1
            else:
                 d[i] = {'td':usl[count],"tw":twl[count],"tm":tml[count],"tos":tosl[count],"ptp":paidl[count],"paidontos":paidontos[count]}
                
    except Exception as e:
        print(e)
    print(today)
    return render(request,"paid.html",{"d":d})



def tvajax(request):
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"

    if request.user.user_level == 9:
        result = LogData.objects.filter(contacted_dt__icontains=current_year_month)
    else:
        result = LogData.objects.filter(caller_name=request.user.username).filter(contacted_dt__icontains=current_year_month)

    result = result.values('agreement_no','sub_disposition').annotate(Count("agreement_no"),Count('sub_disposition')).order_by("-sub_disposition")
    data = list(result.values("sub_disposition","sub_disposition__count"))
    
    con =  LogData.objects.all().values_list('sub_disposition', flat=True).distinct().order_by('sub_disposition')

    main_list = {}

    for i in con:
        main_list[i] = {"a1":0,"a2":0,"a3":0,"a4":0,"a5":0,"a6":0,"a7":0,"a8":0,"a9":0,"a10":0}

    for i in result:
        if i["sub_disposition"] in main_list:
            if i["sub_disposition__count"] == 1:        
                main_list[i["sub_disposition"]]["a1"] += 1
            elif i["sub_disposition__count"] == 2:
                main_list[i["sub_disposition"]]["a2"] += 1
            elif i["sub_disposition__count"] == 3:
                main_list[i["sub_disposition"]]["a3"] += 1
            elif i["sub_disposition__count"] == 4:
                main_list[i["sub_disposition"]]["a4"] += 1
            elif i["sub_disposition__count"] == 5:
                main_list[i["sub_disposition"]]["a5"] += 1
            elif i["sub_disposition__count"] == 6:
                main_list[i["sub_disposition"]]["a6"] += 1
            elif i["sub_disposition__count"] == 7:
                main_list[i["sub_disposition"]]["a7"] += 1
            elif i["sub_disposition__count"] == 8:
                main_list[i["sub_disposition"]]["a8"] += 1
            elif i["sub_disposition__count"] == 9:
                main_list[i["sub_disposition"]]["a9"] += 1
            elif i["sub_disposition__count"] >= 10:
                main_list[i["sub_disposition"]]["a10"] += 1

    data = json.dumps(main_list)
    return JsonResponse({"stat":data})

