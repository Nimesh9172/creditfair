from ..views_imports import *


def total_calls(request):
    upload=0
    available=0
    contacted=0
    noncontacted=0
    try : 
        t=request.GET.get("time")
        print(t,"timeeeeeeeeeeeeeeeeeeee")
        today=datetime.now().date()
        todate=today+timedelta(days=1)
        days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
        monday_date = today - timedelta(days=days_to_monday)
        month = datetime.now().month
        year = datetime.now().year
        current_year_month = f"{year}-{month:02}"
        # print(current_year_month,"total")
        if request.user.user_level == 9:
            lead_data=LeadDetails.objects
            c_nc_data=LeadDetails.objects
        else:
            lead_data=LeadDetails.objects.filter(caller_name=request.user.username)
            c_nc_data=LeadDetails.objects.filter(caller_name=request.user.username)
        
        if t == "today":
            data=Dataupload.objects.filter(entry__icontains=today)
            lead_data=lead_data.filter(list_forkey__entry__icontains=today,attempted=0)
            c_nc_data=c_nc_data.filter(contacted_dt__icontains=today)
            print(c_nc_data,"itssssssssssssssssss today")
        elif t == "week" :
            print(monday_date,today,"in weeek")
            data=Dataupload.objects.filter(entry__range=[monday_date,todate])
            print(data,"uploadddddd")
            lead_data=lead_data.filter(list_forkey__entry__range=[monday_date,todate],attempted=0)
            print(lead_data,"leadddddddddddddddddddddddddddd")
            c_nc_data=c_nc_data.filter(contacted_dt__range=[monday_date,todate])
            print(c_nc_data,"contacteddddddddddddddddd")
        elif t== "month":
            data=Dataupload.objects.filter(entry__icontains=current_year_month)
            lead_data=lead_data.filter(list_forkey__entry__icontains=current_year_month,attempted=0)
            c_nc_data=c_nc_data.filter(contacted_dt__icontains=current_year_month)
            # Total calls upload data starts
        if len(data) != 0 :
            upload=data.aggregate(Sum('count'))
            upload=upload["count__sum"]
        else:
            upload = 0
        # print(upload,data,"after sum")

        #Total calls Available starts
        available=lead_data.count()
        #Total calls Avaialable ends
        
        #Total calls Contacted starts
  
        contacted=c_nc_data.filter(disposition="Contacted").count()
        #Total calls Contacted ends

        #Total calls Non-Contacted starts
        noncontacted=c_nc_data.filter(disposition="Non-Contacted").count()
        #Total calls Non-Contacted ends
    except Exception as e : 
        print(e)
    
    print(upload,available,contacted,noncontacted,"endsssssss")
    return JsonResponse({"status":200,"upload":upload,"available":available,"contacted":contacted,"noncontacted":noncontacted})
   


def agent_available(request):
    try :
        today=datetime.now().date()
        todate=today+timedelta(days=1)
        d=request.GET.get("time")
        month = datetime.now().month
        year = datetime.now().year
        current_year_month = f"{year}-{month:02}"
        days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
        monday_date = today - timedelta(days=days_to_monday)
        if d=="today":
            data=User.objects.filter(user_level=1,date_joined__icontains=today)
        elif d == "week":
            data=User.objects.filter(user_level=1,date_joined__range=[monday_date,todate])
        elif d == "month":
            data=User.objects.filter(user_level=1,date_joined__icontains=current_year_month)
        
        total_agent=User.objects.filter(user_level=1).count()
        logged_in_agent=User.objects.filter(is_loggedin=1).count()
        on_call=data.count()
        on_paused=data.count()
        # print(total_agent,logged_in_agent,on_call,on_paused,"agent info")   
    except Exception as e :
        print(e)
  
    return JsonResponse({"status":200,"total_agent":total_agent,"logged_in_agent":logged_in_agent,"on_call":on_call,"on_paused":on_paused})



def top_five_dispo(request):
    try : 
        today=datetime.now().date()
        todate=today+timedelta(days=1)
        time=request.GET.get("time")
        month = datetime.now().month
        year = datetime.now().year
        current_year_month = f"{year}-{month:02}"
        top5 = LogData.objects
        days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
        monday_date = today - timedelta(days=days_to_monday)
        ls=[]
        # print(today,"weddddddddddddddddddddddddddddd",monday_date)
        if request.user.user_level == 9:
            top5=top5
        else:
            top5=top5.filter(caller_name=request.user.username)
            
        if time == "today":
            top5 = top5.filter(contacted_dt__icontains=today)
            ct=top5.count()
            print(top5,"in today'ssss filter",ct)
            # data=LeadDetails.objects.filter(contacted_dt__icontains=today)
        elif time == "week":
            top5 = top5.filter(contacted_dt__range=[monday_date,todate])
    
        elif time=="month":
            top5=top5.filter(contacted_dt__icontains=current_year_month)
            


        todays_call=top5.count()
        top5 = top5.values('sub_disposition').annotate(count=Count('*')).order_by('-count')[:5]

        # print(todays_call,"todays call",type(todays_call),top5)
        # print('top 5',type(top5),top5[0]["sub_disposition"],top5)
        
        if len(top5) != 0:
            for i in range(len(top5)):
                d={}
                # print("top5[i]['count']",top5[i]["count"],type(top5[i]["count"]))
                if top5[i]["count"] == 0:
                    calc=0
                else:
                    calc=(top5[i]["count"]/todays_call)*100
                
                # print(calc,"just calculated")
                d["Sub_disposition"]=top5[i]["sub_disposition"]

                d["percent"]=str(calc)+"%"
                
                ls.append(d)
        else:
            top5=0

        print(ls,"ls")
    except Exception as e :
        print(e)
    return JsonResponse({"status":200,"ls":ls})
    


def paid_ptp_status(request):
    if request.user.user_level == 9 : 
        paid_data=LogData.objects
        ptp_data=LogData.objects
    else:
        paid_data=LogData.objects.filter(caller_name=request.user.username)
        ptp_data=LogData.objects.filter(caller_name=request.user.username)
    # if request.method == "POST":
    d=request.GET.get("time")
    # print(d,"dddddddddddddddddddddddddddddddddddddddddd")
    today=datetime.now().date()
    todate=today+timedelta(days=1)
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"
    days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
    monday_date = today - timedelta(days=days_to_monday)
    if d=="today":
        paid_data=paid_data.filter(contacted_dt__icontains=today)
        ptp_data=ptp_data.filter(callback_datetime__icontains=today)
    elif d=="week":
        paid_data=paid_data.filter(contacted_dt__range=[monday_date,todate])
        ptp_data=ptp_data.filter(callback_datetime__range=[monday_date,todate])
    elif d=="month":
        paid_data=paid_data.filter(contacted_dt__icontains=current_year_month)
        ptp_data=ptp_data.filter(callback_datetime__icontains=current_year_month)

        
    paid=paid_data.filter(sub_disposition="Paid").count()
    ptp=ptp_data.filter(sub_disposition="Promise To Pay").count()
    # print(ptp,paid,"ptp this")


    return JsonResponse({"status":200,"paid":paid,"ptp":ptp})




def call_status(request):
    d=request.GET.get("time")
    today = timezone.now().date()
    todate=today+timedelta(days=1)
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"
    days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
    monday_date = today - timedelta(days=days_to_monday)
    # print(today,d,"callllllllllllllllllllllstatusssssssssssss")
    time_ranges = [
    (time(9), time(10)),
    (time(10), time(11)),
    (time(11), time(12)),
    (time(12), time(13)),
    (time(13), time(14)),
    (time(14), time(15)),
    (time(15), time(16)),
    (time(16), time(17)),
    (time(17), time(18)),
    (time(18), time(19)),
    
]
    
    if request.user.user_level == 9 :
        data=LogData.objects
    else:
        data=LogData.objects.filter(caller_name=request.user.username)


    print("userrrrrrrrrrrrrrrrrrrr",data)
    if d=="today":
        data=data.filter(contacted_dt__date__icontains=today)
        drop_data=Inbound_log.objects.filter(start__date__icontains=today)
    elif d =="week":
        data=data.filter(contacted_dt__date__range=[monday_date,todate])
        drop_data=Inbound_log.objects.filter(start__date__range=[monday_date,todate])
    elif d=="month":
        # print("in  monthsssssssssssssss")
        data=data.filter(contacted_dt__date__icontains=current_year_month)
        drop_data=Inbound_log.objects.filter(start__date__icontains=current_year_month)
        # print(drop_data,"missssssssssss")

    out_call_9_10=data.filter(contacted_dt__time__range=time_ranges[0],direction="Out").count()
    out_call_10_11=data.filter(contacted_dt__time__range=time_ranges[1],direction="Out").count()
    out_call_11_12=data.filter(contacted_dt__time__range=time_ranges[2],direction="Out").count()
    out_call_12_1=data.filter(contacted_dt__time__range=time_ranges[3],direction="Out").count()
    out_call_1_2=data.filter(contacted_dt__time__range=time_ranges[4],direction="Out").count()
    out_call_2_3=data.filter(contacted_dt__time__range=time_ranges[5],direction="Out").count()
    out_call_3_4=data.filter(contacted_dt__time__range=time_ranges[6],direction="Out").count()
    out_call_4_5=data.filter(contacted_dt__time__range=time_ranges[7],direction="Out").count()
    out_call_5_6=data.filter(contacted_dt__time__range=time_ranges[8],direction="Out").count()
    out_call_6_7=data.filter(contacted_dt__time__range=time_ranges[9],direction="Out").count()

    In_call_9_10=data.filter(contacted_dt__time__range=time_ranges[0],direction="In").count()
    In_call_10_11=data.filter(contacted_dt__time__range=time_ranges[1],direction="In").count()
    In_call_11_12=data.filter(contacted_dt__time__range=time_ranges[2],direction="In").count()
    In_call_12_1=data.filter(contacted_dt__time__range=time_ranges[3],direction="In").count()
    In_call_1_2=data.filter(contacted_dt__time__range=time_ranges[4],direction="In").count()
    In_call_2_3=data.filter(contacted_dt__time__range=time_ranges[5],direction="In").count()
    In_call_3_4=data.filter(contacted_dt__time__range=time_ranges[6],direction="In").count()
    In_call_4_5=data.filter(contacted_dt__time__range=time_ranges[7],direction="In").count()
    In_call_5_6=data.filter(contacted_dt__time__range=time_ranges[8],direction="In").count()
    In_call_6_7=data.filter(contacted_dt__time__range=time_ranges[9],direction="In").count()
    # print(drop_data,"starts")
    drop_call_9_10=drop_data.filter(start__time__range=time_ranges[0]).count()
    drop_call_10_11=drop_data.filter(start__time__range=time_ranges[1]).count()
    drop_call_11_12=drop_data.filter(start__time__range=time_ranges[2]).count()
    drop_call_12_1=drop_data.filter(start__time__range=time_ranges[3]).count()
    drop_call_1_2=drop_data.filter(start__time__range=time_ranges[4]).count()
    drop_call_2_3=drop_data.filter(start__time__range=time_ranges[5]).count()
    drop_call_3_4=drop_data.filter(start__time__range=time_ranges[6]).count()
    drop_call_4_5=drop_data.filter(start__time__range=time_ranges[7]).count()
    drop_call_5_6=drop_data.filter(start__time__range=time_ranges[8]).count()
    drop_call_6_7=drop_data.filter(start__time__range=time_ranges[9]).count()
    # print(time_ranges,"kskdnad")
    print(out_call_9_10,out_call_10_11,out_call_11_12,out_call_12_1,out_call_1_2,out_call_2_3,out_call_3_4,out_call_4_5,out_call_5_6,out_call_6_7)
    print(In_call_9_10,In_call_10_11,In_call_11_12,In_call_12_1,In_call_1_2,In_call_2_3,In_call_3_4,In_call_4_5,In_call_5_6,In_call_6_7)

    print(drop_call_9_10,drop_call_10_11,drop_call_11_12,drop_call_12_1,drop_call_1_2,drop_call_2_3,drop_call_3_4,drop_call_4_5,drop_call_5_6,drop_call_6_7)

    return JsonResponse({"status":200,"out_call_9_10":out_call_9_10,"out_call_10_11":out_call_10_11,"out_call_11_12":out_call_11_12,"out_call_12_1":out_call_12_1,"out_call_1_2":out_call_1_2,"out_call_2_3":out_call_2_3,"out_call_3_4":out_call_3_4,"out_call_4_5":out_call_4_5,"out_call_5_6":out_call_5_6,"out_call_6_7":out_call_6_7,"In_call_9_10":In_call_9_10,"In_call_10_11":In_call_10_11,"In_call_11_12":In_call_11_12,"In_call_12_1":In_call_12_1,
    "In_call_1_2":In_call_1_2,"In_call_2_3":In_call_2_3,"In_call_3_4":In_call_3_4,"In_call_4_5":In_call_4_5,"In_call_5_6":In_call_5_6,"In_call_6_7":In_call_6_7,"drop_call_9_10":drop_call_9_10,"drop_call_10_11":drop_call_10_11,"drop_call_11_12":drop_call_11_12,"drop_call_12_1":drop_call_12_1,"drop_call_1_2":drop_call_1_2,"drop_call_2_3":drop_call_2_3,"drop_call_3_4":drop_call_3_4,"drop_call_4_5":drop_call_4_5,"drop_call_5_6":drop_call_5_6,"drop_call_6_7":drop_call_6_7})
