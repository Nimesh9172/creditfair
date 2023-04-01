from ..views_imports import *


def timeaddition(ls):
    if len(ls)==0:
        return "0:00:00"
    sumup = timedelta()
    for i in ls:
        (h, m, s) = i.split(':')
        d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        sumup += d
    return sumup

def timediffernece(t1,t2):
    format = '%H:%M:%S'
    difference = datetime.strptime(t1, format) - datetime.strptime(t2, format)
    return difference

def convert_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, remaining_seconds)

def test(request):
    return render(request,"test.html")

def call_apr(request):
    return JsonResponse({"status":200})

def hangup_apr(request):
    return JsonResponse({"status":300})

def dispose_apr(request,id):
    try:
        print("dispoooooseeeeeeeaprrrrrrrrrrrr")
        current_date =datetime.now().date()
        extid = request.user.extension
        username = request.user.username
        forkey = id

        query = agentevents.objects.filter(agentname=username,call_time__icontains=current_date).last()
        current_calltime = query.call_time.time().strftime("%H:%M:%S")
        current_hanguptime = query.hang_time.time().strftime("%H:%M:%S")
        current_disposition_time = query.disposed_time.time().strftime("%H:%M:%S")
        current_date =datetime.now().date()

        query2 = agent_performance.objects.filter(agentname=username,event_date= current_date).last()

        #//////////////////////getting wrap-up time////////////
        print(current_hanguptime,current_disposition_time,"dospossssstimeeeeee")
        wrapup_time = timediffernece(current_disposition_time,current_hanguptime)
        prev_wrapup_time = query2.wrap_up
        wrapup_time_list = [str(wrapup_time),str(prev_wrapup_time)]
        wrapup_time_sumup = timeaddition(wrapup_time_list)

        print(wrapup_time,wrapup_time_list,current_disposition_time,current_hanguptime,"wrappptimeeeee") 

        # /////////////////////getting talktime//////////////////
        # query3 = CallRecording.objects.filter(callid=query.call_id).last()
        # print(query3,"query3333333333")
        # if not query3:
        #     talktime = 0
        # else:
        #     talktime = convert_seconds(query3.billsec)

        # prev_talktime = query2.talk_time
        # talktime_time_list = []
        # talktime_time_list.append(str(talktime))
        # talktime_time_list.append(str(prev_talktime))

        # Addition of calltime and hangtime starts
        time_diff=timediffernece(current_hanguptime,current_calltime)
        previous_time = query2.talk_time
        totaltalktime=timeaddition([str(time_diff),previous_time])
        # print('time difference',time_diff,previous_time,totaltime,totaltime)
        # print('timeeeeeeeeeeeeeeeeeeeee',totaltime,time_diff,previous_time)
        time_diff2=timediffernece(current_disposition_time,current_hanguptime)
        previouswraptime=query2.wrap_up
        totalwraptime=timeaddition([str(time_diff2),previouswraptime])
        agent_performance.objects.filter(id=query2.id).update(talk_time=totaltalktime,wrap_up=totalwraptime)
        # Addition of calltime and hangtime ends


        talktime_time_sumup = "0:00:00"

        # agent_performance.objects.filter(id=query2.id).update(wrap_up=wrapup_time_sumup,talk_time=talktime_time_sumup)

        #update idletime if 2nd time calling else update nonactive events
        query4 = agentevents.objects.filter(agentname=username,call_time__icontains=current_date).order_by('-id')
        prev_call_tof = True
        # print(query4,"queryy4444444444")
    except Exception as e:
        print(e)
    
    try:
        query4 = query4[1]
    except Exception as e:
        print(e)
        prev_call_tof = False

    # print(query4,"queryy4444444444ttttttttt")

    if prev_call_tof:
        # print("idle timee")
        prev_idletime = query2.idle_time
        prev_calltime = query4.disposed_time.time().strftime("%H:%M:%S")
        idletime = timediffernece(current_calltime,prev_calltime)
        idletime_list = []
        idletime_list.append(str(prev_idletime))
        idletime_list.append(str(idletime))
        idle_time_sumup = timeaddition(idletime_list)

        # print(prev_idletime,prev_calltime,idletime_list)

        agent_performance.objects.filter(id=query2.id).update(idle_time=idle_time_sumup,active_status="active")

    else:
        # print("no prev called")
        login_time = query2.date_time_added.time().strftime("%H:%M:%S")
        prev_nonactive_hrs = query2.nonactive_hrs
        nonactive_hrs = timediffernece(current_calltime,login_time)
        nonactive_hrs_list = []
        nonactive_hrs_list.append(str(prev_nonactive_hrs))
        nonactive_hrs_list.append(str(nonactive_hrs))
        # print(nonactive_hrs_list)
        nonactive_hrs_sumup = timeaddition(nonactive_hrs_list)

        agent_performance.objects.filter(id=query2.id).update(nonactive_hrs=nonactive_hrs_sumup,active_status="active")
        # start with logout
        print(nonactive_hrs,current_calltime,login_time,nonactive_hrs_sumup)

      # login hours calculation
    query6 = agent_performance.objects.filter(id=query2.id).last()
    #All variables for login time calculation
    hold_hrs_log = query6.hold_hours
    nonactive_hrs_log = query6.nonactive_hrs
    break_hours_log = query6.break_hours
    idletime_log =  query6.idle_time
    login_hrs_list = []
    tos_list=[]
    login_hrs_list.append([hold_hrs_log,nonactive_hrs_log,break_hours_log,idletime_log,str(totaltalktime),str(wrapup_time_sumup)])
    tos_list.append([hold_hrs_log,idletime_log,str(totaltalktime),str(wrapup_time_sumup)])
    print(login_hrs_list,"listsstsstststs")
    logintime_sumup = timeaddition(login_hrs_list[0])
    tos_sumup = timeaddition(tos_list[0])

    agent_performance.objects.filter(id=query2.id).update(login_hours=logintime_sumup,tos=tos_sumup,last_event="call")
    
    print(logintime_sumup,"logggigngigngisumupppppppppppppp")
    # print(ringing_time,prev_ringingtime,type(prev_ringingtime))


    
    return JsonResponse({"status":200})


def login_apr(request):
    current_date =datetime.now().date()
    username = request.user.username
    entry = datetime.now()
    query = agent_performance.objects.filter(agentname=username,event_date=current_date)
    if query.exists():
        print("exists")
        query.update(date_time_added=entry,last_event='login')
    else:
        agent_performance.objects.create(agentname=request.user.username,event_date=current_date,last_event='login')
        print("created")
    
    return JsonResponse({"status":200})

def logout_apr(request):
    username = request.user.username
    current_date =datetime.now().date()
    current_time =datetime.now().time().strftime("%H:%M:%S")

    query =  agent_performance.objects.filter(agentname=username,event_date=current_date)

    # login_time = "00:00:00"
    if query:
        login_time = query.last().date_time_added.time()    

    # print(login_time)

    if query and query.last().active_status == "inactive":
        print("inactive")
        login_time = login_time.strftime("%H:%M:%S")

        format = '%H:%M:%S'
        time_difference = datetime.strptime(current_time, format) - datetime.strptime(login_time, format)
        print(current_time,login_time,time_difference,"curenttimeeeee")
        nonactive_hrs = query.last().nonactive_hrs

        timeList = []
        timeList.append(str(nonactive_hrs))
        timeList.append(str(time_difference))
       
        mysum = timedelta()
        for i in timeList:
            (h, m, s) = i.split(':')
            d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            mysum += d
        
        prev_login_hrs = query.last().login_hours
        login_hrs_list = []
        login_hrs_list.append(str(time_difference))
        login_hrs_list.append(str(prev_login_hrs))
        login_hrs_sumup = timeaddition(login_hrs_list)

        print(nonactive_hrs,time_difference,timeList,login_time,mysum,login_hrs_sumup,login_hrs_list,"inactivee")
        query.update(nonactive_hrs = mysum,login_hours=login_hrs_sumup)
    else:
        print("active")
        query3 = agentevents.objects.filter(agentname=username,call_time__icontains=current_date).last()
        query4 = break_details.objects.filter(agentname=username,break_start__icontains=current_date).last()
        prev_dispose_time = None
        break_time = None
        start_time = None

        if query3:
            prev_dispose_time = query3.disposed_time

        if query4:
            break_time = query4.break_end

        if prev_dispose_time and break_time:
            if prev_dispose_time > break_time:
                start_time = prev_dispose_time
                print("dispoesdd")
            else:
                start_time = break_time
                print("break")
        elif not prev_dispose_time and not break_time:
            if not query:
                start_time = None
            else:    
                start_time = query.last().date_time_added
                print("no dispose and break")
        elif prev_dispose_time:
            start_time = prev_dispose_time
            print("prev_dispose")
        elif break_time:
            start_time = break_time
            print("breakk")
        else:
            start_time = query.last().date_time_added
            print("elsee")
        
        print(start_time,prev_dispose_time,break_time)

        
        if start_time:
            start_time = start_time.time().strftime("%H:%M:%S")
            idle_time = timediffernece(current_time[:8],start_time)
            prev_idletime = query.last().idle_time
            idletime_list = []
            idletime_list.append(str(idle_time))
            idletime_list.append(str(prev_idletime))
            idletime_sumup = timeaddition(idletime_list)

            prev_login_hrs = query.last().login_hours   
            login_hrs_list = []
            login_hrs_list.append(str(idle_time))
            login_hrs_list.append(str(prev_login_hrs))
            login_hrs_sumup = timeaddition(login_hrs_list)


            # ///////tos /////////
            prev_tos = query.last().tos
            tos_list = []
            tos_list.append(str(prev_tos))
            tos_list.append(str(idle_time))
            tos_sumup = timeaddition(tos_list)


            query.update(idle_time = idletime_sumup,login_hours=login_hrs_sumup,tos=tos_sumup,active_status="inactive")
            print(idletime_list,idletime_sumup,login_hrs_list,login_hrs_sumup)

       
       
    return JsonResponse({"status":200})



def apr_report_export(request):
    username = request.POST.get('username')
    # username = "admin"
    current_date = datetime.now().date()
    print(username)

    # query2 = dispositions_count.objects
        
    dispo_query = LogData.objects.all().values_list('sub_disposition', flat=True).distinct().order_by('sub_disposition')
    break_details_query = infobreak.objects

    user_ls = agent_performance.objects 
    read = agent_performance.objects

    date_range = ["2023-02-1","2024-02-24"]

    if username == "all":
        user_ls = user_ls.filter(event_date__range=date_range)
        read = read.filter(event_date__range=date_range)
        break_details_query = break_details_query.filter(date__range=date_range)
    else:
        user_ls = user_ls.filter(agentname=username)
        read = read.filter(agentname=username)
        break_details_query = break_details_query.filter(agentname=username)

    user_ls = user_ls.values_list('agentname', 'event_date').order_by('agentname')
    break_details_query =  break_details_query.values_list('name', flat=True).distinct().order_by('name')
    
    print(user_ls,"lssssssssslssl")

    ls = []
    total_call_count = []
    dispo_dict={}


    for i in range(len(user_ls)):
        print(user_ls[i][1],"sdasa")
        query = LogData.objects.filter(caller_name=user_ls[i][0],contacted_dt__icontains=user_ls[i][1])
        total_call_count.append(len(query))
        dispo_dict = dispo_dict.fromkeys(dispo_query,0)
        for i in query:
           dispo_dict[i.sub_disposition] += 1
            
        ls.append(dispo_dict)

    print(ls,"dictsssss")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') 

    row_num = 0

    columns = ["Agent Name","Date","Login Hours","Idle hours","Talk Hours","Wrap-up Hours","Break Hours","TOS (Time on system)","Non-active Hours"]

    col_num_value = 0
    col_num_key = 0
    dispo_col_num_value = 0
    for col_num in range(len(columns)):
        col_num_key += 1
        col_num_value += 1
        dispo_col_num_value += 1
        ws.write(row_num, col_num, columns[col_num])


    # //////////// break keys start////////
    for col_num in range(len(break_details_query)):
        ws.write(row_num,col_num_key,break_details_query[col_num])
        col_num_key+=1
        col_num_value += 1
    # //////////// break keys end////////
    
    # //////////total calls key//////////
    ws.write(row_num,col_num_key,"Total Calls")
    col_num_key += 1
    col_num_value += 1
    # //////////total calls key//////////

    #////// disposition keys start///////
    # for col_num in dict:
    for col_num in range(len(dispo_query)):
        ws.write(row_num,col_num_key,dispo_query[col_num])
        col_num_key+=1

    #////// disposition keys end///////

    rows = read.values_list("agentname","event_date","login_hours","idle_time","talk_time","wrap_up","break_hours","tos","nonactive_hrs")

    # ///////////////////////////agent performance values append in excel//////////////////////////
    row_num1 = 0
    for row in rows:
        row_num1 += 1
        for col_num in range(len(row)):
            data=str(row[col_num]).replace("nan"," ")
            data=data.replace("None"," " )
            ws.write(row_num1,col_num,data)
    # ///////////////////////////agent performance values append in excel//////////////////////////

    # //////////////////// subdisposition append in excel////////////
    for row in range(len(ls)):
        row_num += 1
        temp_col_num = col_num_value
        ws.write(row_num,col_num_value-1,total_call_count[row])
        for col_num in ls[row]:
            data=str(ls[row][col_num]).replace("nan"," ")
            data=data.replace("None"," ")
            ws.write(row_num,temp_col_num,ls[row][col_num])
            print(row_num,temp_col_num,ls[row][col_num])
            temp_col_num += 1  
    # //////////////////// subdisposition append in excel //////////// 

    # ///////////////////// break append in excel////////////
    row_num2 = 0 
    for i in user_ls:
        row_num2 += 1
        temp_col_num2 = dispo_col_num_value
        inbk = infobreak.objects.filter(agentname=i[0],date=i[1])
        for j in inbk:
            print(row_num2,temp_col_num2,j.total)
            ws.write(row_num2,temp_col_num2,j.total)
            temp_col_num2 += 1
    # ///////////////////// break append in excel//////////////////

    wb.save(response)

    return response
    return JsonResponse({"status":200})

def break_events(request):
    if request.method == "POST":
        username =request.user.username
        event=request.POST.get("event")
        b_type=request.POST.get("type")

        current_dt = datetime.now()
        current_d = datetime.now().date()
        current_t = current_dt.time().strftime("%H:%M:%S")

        if event == "start": 
            break_details.objects.create(agentname=username,break_start=current_dt,break_end = current_dt,break_name=b_type)

        elif event == "end":
            b_start =  break_details.objects.filter(agentname = username,break_start__icontains = current_d,break_name=b_type).last()
            b_start_time = b_start.break_start.time().strftime("%H:%M:%S")
            total_break_time = timediffernece(current_t,b_start_time) 
            break_details.objects.filter(id = b_start.id).update(break_end=current_dt,break_total=total_break_time)

            # ////////////////////////// insert the sum up of break in agentperformance table///////////////////
            agn_p=agent_performance.objects.filter(agentname=request.user.username,event_date=current_d).last()

                # //////////////////////gap between login and break time////////////////////
            gap="00:00:00"
            if agn_p.last_event == "login":
                prev_time = agn_p.date_time_added.time().strftime("%H:%M:%S")
                gap = timediffernece(current_t,str(prev_time))
                agent_performance.objects.filter(id=agn_p.id).update(nonactive_hrs=gap)

            elif agn_p.last_event == "call":
                query = agentevents.objects.filter(agentname=request.user.username,disposed_time__icontains=current_d).last()
                prev_time = query.disposed_time.time().strftime("%H:%M:%S")
                prev_idle_time = agn_p.idle_time
                gap = timediffernece(current_t,str(prev_time))
                idle_time_gap_sum = timeaddition([str(gap),prev_idle_time])
                agent_performance.objects.filter(id=agn_p.id).update(idle_time=idle_time_gap_sum)
           
            elif agn_p.last_event == "break":
                query2 = break_details.objects.filter(agentname=request.user.username,break_end__icontains=current_d).order_by('-id')
                print(query2,"qqqqqqq2222222222")   
                prev_end_time = query2[1].break_end.time().strftime("%H:%M:%S")
                current_start_time = query2.first().break_start.time().strftime("%H:%M:%S")
                prev_idle_time=agn_p.idle_time
                gap = timediffernece(str(current_start_time),str(prev_end_time))
                idle_time_gap_sum = timeaddition([str(gap),prev_idle_time])
                print([str(gap),prev_idle_time],"breakkkkkkinggg")
                agent_performance.objects.filter(id=agn_p.id).update(idle_time=idle_time_gap_sum)

                # ////////////login hrs sumup
            login_hrs = agn_p.login_hours 
            login_hrs_sumup = timeaddition([str(login_hrs),str(total_break_time),str(gap)])

                #//////////////////////// breakhrs sumup//////////////////
            prev_break_hrs = agn_p.break_hours
            break_hrs_sumup = timeaddition([str(prev_break_hrs),str(total_break_time)])
            print([str(login_hrs),str(total_break_time)],[str(prev_break_hrs),str(total_break_time)])
            agent_performance.objects.filter(id=agn_p.id).update(login_hours=login_hrs_sumup,break_hours=break_hrs_sumup,last_event="break")

            # ///////////////////insert the sum up of break in infobreak table///////////////////////
            ib_query =  infobreak.objects.filter(agentname=request.user.username,date=current_d,name=b_type).last()
            print(ib_query)
            if not ib_query:
                infobreak.objects.create(agentname=request.user.username,date=current_d,name=b_type,total=total_break_time)
            else:
                info_prev_break_hrs = ib_query.total
                info_break_sumup = timeaddition([str(info_prev_break_hrs),str(total_break_time)])
                print(info_break_sumup,"info_breakkksumupppp")
                infobreak.objects.filter(id=ib_query.id).update(total=info_break_sumup)


        print(event,b_type)
       
    return JsonResponse({"status":200})
 
