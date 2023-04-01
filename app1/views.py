from .views_imports import *

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'dashboard/dashboard.html')

def lead_behaviour(request):
    return render(request,"teamoverall/leadbehaviour.html")

def ptp_status(request):
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
    # return JsonResponse({"d":d})
    return render(request,"teamoverall/ptp_status.html",{"d":d})

def paid_status(request):
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
        paid=LogData.objects.filter(caller_name=i.username).filter(sub_disposition="Paid").filter(contacted_dt__range=[today,this_month]).aggregate(Sum('amount'))
        p=paid['amount__sum']
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
    return render(request,"teamoverall/paid_status.html",{"d":d})



def dispo_status(request):
    return render(request,"teamoverall/dispo_status.html")


@login_required(login_url="login")
def reminder(request):
    return render(request,"reminder/reminder.html")

@login_required(login_url="login")
def recovery(request):
    dispo=disposition.objects.exclude(sub_dispo__in=["Call Back","Promise To Pay","Schedule Call"])
    return render(request,"recovery/recovery.html",{"dispo":dispo})

@login_required(login_url="login")
def missedcall(request):
    return render(request,"missedcall/missedcall.html")

@login_required(login_url="login")
def ots(request):
    return render(request,"ots/ots.html")

@login_required(login_url="login")
def non_attempted(request):
    u=User.objects.filter(user_level=1)
    l_id=Dataupload.objects.all()
    data=LeadDetails.objects.filter(caller_name=request.user.username,attempted=0).exclude(list_forkey__status__contains="0")
    if request.user.user_level == 9:
        print("noatp first if")
        data=LeadDetails.objects.filter(attempted=0).exclude(list_forkey__status__contains="0")
    if request.method=="POST":
        print("noatp sec if")
        agent=request.POST.get("agent")
        list_id=request.POST.get("list_id")
        if request.user.user_level == 1:
            agent = request.user.username
        print("itssssss",list_id,agent)
        if list_id != ""  and list_id != "all":
            try:
                list_id = data.filter(list_id=list_id).last().list_id_id
                print('hgfhgfhgfhgf',list_id,"asdnaiuhdahdashoiasfoauf9auf9ausfsafasfu ")
            except Exception as e:
                print(e)
            print(list_id)
            data=data.filter(list_id=list_id)
        if agent != "all" and agent != "":
            print("agentttttt",agent)
            data = data.filter(caller_name=agent)
        data= data.filter(attempted=0).exclude(list_forkey__status__contains="0")[:1000]
        print("asdas",  data)
        return JsonResponse({"data":list(data.values())})
    return render(request,"non_attempted/non_attempted.html",{"u":u,"l_id":l_id})

@login_required(login_url="login")
def quality(request):
    d=disposition.objects.all()
    u=User.objects.all()
    return render(request,"quality/quality.html",{"d":d,"u":u})

@login_required(login_url="login")
def score_card(request,id):
    s=Score.objects.filter(qs_id=id)
    print(s,"scoredata")
    return render(request,"quality/score.html",{"s":s})

@login_required(login_url="login")
def qualityexport(request):
    u=User.objects.all()
    return render(request,"quality/qexport.html",{"u":u})



@login_required(login_url="login")
def connect_to_customer(request):
    return render(request,"connect_to_customer/connect_to_customer.html")

@login_required(login_url="login")
def leadupdate(request):
    return render(request,"leadupdate/leadupdate.html")

@login_required(login_url="login")
def dnd(request):
    return render(request,"dnd/dnd.html")

@login_required(login_url="login")
def sms(request):
    return render(request,"sms/sms.html")


def get_dispositions(request):
    
    dispo = disposition.objects.all().values('dispo').distinct()
    dispo = DispositionsSerializers(dispo,many=True)

    # sdispo =  disposition.objects.all()
    sub_val = request.GET.get('dispo')
    # if sub_val:
    sdispo = disposition.objects.filter(dispo=sub_val)

    sdispo = SubDispositionsSerializers(sdispo,many=True) 
    return JsonResponse({'status':200,'disposition':dispo.data,'subdisposition':sdispo.data})