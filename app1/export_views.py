from .models import *
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from datetime import datetime,timedelta
import xlwt



def export_reminder(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    if request.user.user_level == 9:
        all_data=LeadDetails.objects.filter(callback_datetime__contains=d4).filter(Q(sub_disposition='Promise To Pay') | Q(sub_disposition='Call Back')| Q(sub_disposition='Schedule Call'))
        print("99999999999999",all_data)
    if request.method == "POST":
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('todate').rstrip()
        fil = request.POST.get('filterval')
        fil = fil.split(",")
        sortval = request.POST.get('sortby') 
        print("filll",fil)
        try:

            if fd != "" and td != "":
                fd = datetime.strptime(fd,'%d-%m-%Y')
                td = datetime.strptime(td,'%d-%m-%Y')
                if fd != td:
                    td = td + timedelta(days=1)
                    
                fd = fd.strftime("%Y-%m-%d")
                td = td.strftime("%Y-%m-%d")
                if request.user.user_level == 9:
                    all_data=LeadDetails.objects.filter(Q(sub_disposition='Promise To Pay') | Q(sub_disposition='Call Back')| Q(sub_disposition='Schedule Call'))
                    
                else:
                    all_data = LeadDetails.objects.filter(caller_name=request.user.username).filter(Q(sub_disposition='Promise To Pay') | Q(sub_disposition='Call Back')| Q(sub_disposition='Schedule Call'))

                if fd == td:
                    all_data = all_data.filter(callback_datetime__icontains=fd)
                    
                else:
                    
                    all_data = all_data.filter(callback_datetime__range=[fd,td])
                    print("inssisiisisisis",all_data)
           
            if sortval != '':
                if sortval == "ascending":
                    all_data = all_data.order_by('TOS')
                elif sortval == "descending":
                    all_data = all_data.order_by('-TOS')    
            if fil != ['']:
                all_data = all_data.filter(Q(sub_disposition__in=fil))

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')

            row_num = 0

            columns = ["Name","Agreement No.","Amount","Disposition","Date&Time","Caller ID"]
            
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num]) 
            
            rows = all_data.values_list("name","agreement_no","main_amount","sub_disposition","callback_datetime","caller_name")

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                  
                    data=str(row[col_num]).replace("nan"," ")
                    data=data.replace("None"," " )
                    if col_num == 4:
                        data = str(row[col_num])[:19]
                    ws.write(row_num, col_num,data)
            wb.save(response)

            print(response)
            return response

        except  Exception as e:
            print(e)
            
    print("all_data",all_data)
    return JsonResponse({'status':200})



def export_recovery(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    data=LeadDetails.objects
    if request.user.user_level == 9:
        data=LeadDetails.objects.exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)
    else:
        data=LeadDetails.objects.filter(caller_name=request.user.username).exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)

    if request.method == "POST":
        
        fd = request.POST.get('fdate')
        td = request.POST.get('tdate')
        sel = request.POST.get('sortval')
        
        print(fd,td,sel,"parameters")
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
                
          
            if sel != None:
                sel = sel.split(",")
                data = data.filter(Q(sub_disposition__in=sel))

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')

            row_num = 0

            columns = ["Name","Agreement No.","Amount","Contacted DateTime","Sub Disposition","Caller ID"]
            
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num]) 
            
            rows = data.values_list("name","agreement_no","main_amount","contacted_dt","sub_disposition","caller_name")

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                  
                    data=str(row[col_num]).replace("nan"," ")
                    data=data.replace("None"," " )
                    if col_num == 4:
                        data = str(row[col_num])[:19]
                    ws.write(row_num, col_num,data)
            wb.save(response)

            print(response)
            return response

        except  Exception as e:
            print(e)
            
    print("all_data",data)
    return JsonResponse({'status':200})



def export_misscall(request):
        
    todaydate = datetime.today().strftime("%Y-%m-%d")   
     #todaydate = "2022-09-19"
   
    if request.method=="POST":
        sd=request.POST.get("fdate").rstrip()
        ed=request.POST.get("todate").rstrip()
        sd=datetime.strptime(sd,'%d-%m-%Y')
        ed=datetime.strptime(ed,'%d-%m-%Y')
    
        sd=sd.strftime("%Y-%m-%d")
        ed=ed.strftime("%Y-%m-%d")
        filt = request.POST.get("filter")

        today=datetime.now().date()
        print(today)
    
        if request.user.user_level == 9:
            miss=Inbound_log.objects.filter(start__contains=today)
        else:
            print("else",request.user.username)
            miss=Inbound_log.objects.filter(start__contains=today)

        if request.user.user_level == 9: 
            miss=Inbound_log.objects.filter(start__range=[sd,ed])
            if sd == ed:
               miss=Inbound_log.objects.filter(start__contains=ed)
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
            miss = miss.filter(status  = "Ringing No Response")

        # miss = miss[:150]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Contact no.","Misscall Date","Misscall Count","Status"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = miss.values_list("src","start","count","status")

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                print(row[col_num])
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," ")
                # if col_num == 5:
                #     data = str(row[col_num])[:19]
                ws.write(row_num, col_num,data)
        wb.save(response)
        
        return response

    
    return JsonResponse({"miss":list(miss.values())})



def export_qualityscore(request):
    data=CallRecording.objects   
    todaydate = datetime.today().strftime("%Y-%m-%d")   
     #todaydate = "2022-09-19"
    if request.method=="POST":
        fd=request.POST.get("fdate")
        td=request.POST.get("todate")
        process=request.POST.get("process")
        agn=request.POST.get("agent")
        dispo=request.POST.get("dispo")
        phone_no = request.POST.get('phone_num')
        print(dispo,agn,"quality parameters",fd,td,phone_no,process)
        data = data.filter(id__isnull = False )
        if agn == "all" and agn !="":
            data=data.all()
        elif agn!='all' and agn !='':
                data=data.filter(agentname=agn)
                print("agnnnnn",data)
        if dispo == 'all':
            data = data.all()
            print("disp filter",dispo,data)
        elif dispo !="all" and dispo !="":
            data = data.filter(sub_dispos = dispo)

        if fd != "" and td != "":
            print(data,"ffffffffffffdtdddddddddddddddddddddd")
            fd = datetime.strptime(fd,'%d-%m-%Y')
            td = datetime.strptime(td,'%d-%m-%Y')
            if fd != td:
                td = td + timedelta(days=1)
                data=data.filter(start__range=[fd,td])
                print("fd td not empty",data)
            fd = fd.strftime("%Y-%m-%d")
            td = td.strftime("%Y-%m-%d")

        if fd == td:
            print("sameeeeeeeeeeeeeeeeeeeeee",data)
            data = data.filter(start__icontains=td)
            print("both are same",data)       


        if phone_no!= "":
            print("phone not empty",phone_no)
            data=data.filter(Q(src__icontains=phone_no)|Q(dst__icontains=phone_no))
            print(data,"after")
    # miss = miss[:150]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Agent Name","Direction","Source",'Destination',"Dispositon","Date & Time","Call Recording"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = data.values_list("agentname","direction","src","dst","sub_dispos","start","recordfile")

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," ")
                # if col_num == 5:
                #     data = str(row[col_num])[:19]
                ws.write(row_num, col_num,data)
        wb.save(response)
        
        return response

    
    return JsonResponse({"miss":list(data.values())})
