from ..views_imports import *

#//////////////////Quality Score card starts////////////////

def qsajax(request):
    data = CallRecording.objects
    if request.method == "POST":
        fd=request.POST.get("fdate")
        td=request.POST.get("tdate")
        process=request.POST.get("process")
        agn=request.POST.get("agn")
        dispo=request.POST.get("dispo")
        phone_no = request.POST.get('phone_no')
        print(dispo,agn,"quality parameters",fd,td,phone_no,process)
        data = data.filter(id__isnull = False )
        if agn == "all" and agn !="":
            data=data.all()
            print("in all")
        elif agn!='all' and agn !='':
                # data = data.filter(agentname=agn)
                # print(data)
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
                td=td+ timedelta(days=1)
                data=data.filter(start__range=[fd,td])
                print("fd td not empty",data)
            fd = fd.strftime("%Y-%m-%d")
            td = td.strftime("%Y-%m-%d")

            if fd == td:
                print("sameeeeeeeeeeeeeeeeeeeeee",td)
                data = data.filter(start__icontains=td)
                print("both are same",data,td)       


        if phone_no!= "":
            print("phone not empty",phone_no)
            data=data.filter(Q(src__icontains=phone_no)|Q(dst__icontains=phone_no))
            print(data,"after")

        data = data.order_by("-id")
        # print(agn,dispo,fd,td,phone_no)
        print(data,"final")
    return JsonResponse({"status":200,"data":list(data.values())})





def scoredata(request):
    if request.method=="POST":
        phno = request.POST.get("phno")
        agn=request.POST.get("agn")
        sub=request.POST.get("sub")
        dispo=request.POST.get("dispo")
        contact=request.POST.get("contact")
        id=request.POST.get("id")
        rec=request.POST.get("rec")
        up=datetime.now().date()

        print("test",id,rec,"POST from qsajax")
        if Score.objects.filter(qs_id=id).exists():
            print("in if",id)
            qs=Score.objects.filter(qs_id=id).update(agent=agn,direction=dispo,contacted_dt=contact,recordingfile=rec,phone=phno,sub=sub)
        else:
            print(id,"in else")
            qs=Score.objects.create(agent=agn,direction=dispo,contacted_dt=contact,recordingfile=rec,phone=phno,sub=sub,qs_id=id)
            qs.save()
        print("from here")
        return JsonResponse({"id":id,"status":200})
    

def score(request):
    print("from function")
    if request.method == "POST":
        print("here in post")
        id=request.POST.get("id")
        m1=request.POST.get("1st")
        m2=request.POST.get("2nd")
        m3=request.POST.get("3rd")
        m4=request.POST.get("4th")
        m5=request.POST.get("5th")
        m6=request.POST.get("6th")
        m7=request.POST.get("7th")
        m8=request.POST.get("8th")
        m9=request.POST.get("9th")
        total=request.POST.get("tot")
        got=request.POST.get("got")
        per=request.POST.get("per")
        ls=request.POST.get("ls")
        ls = ls.split(',')
        dt=datetime.now()
        print(ls)
        print(type(ls))
        q=Score.objects.filter(id=id)
        q.update(lastupdate=dt,gm1=m1,gm2=m2,gm3=m3,gm4=m4,gm5=m5,gm6=m6,gm7=m7,gm8=m8,gm9=m9,total=total,got=got,performance=per,m1=ls[0],m2=ls[1],m3=ls[2],m4=ls[3],m5=ls[4],m6=ls[5],m7=ls[6],m8=ls[7],m9=ls[8])
        
        print(m1,m2,m3,m4,m5,m6,m7,m8,m9,total,got,per,ls)
        return JsonResponse({"status":200})
    return JsonResponse({"status":400})
    


def qsexport(request):
    if request.method == "POST":
        pro_sel=request.POST.get("process")
        agn_sel=request.POST.get("agn_sel")
        criteria_sel=request.POST.get("cri_sel")
        fdate=request.POST.get("fdate")
        tdate=request.POST.get("todate")
        data=Score.objects
        print(pro_sel,"agn",agn_sel,'criiiii',criteria_sel,"fdddddd",fdate,tdate,"all parameters")
        print(data)
        if pro_sel!="" and pro_sel =="all":
            data=data.all()
            print("in pro")

        # if pro_sel !="" and pro_sel !="all":
        #     data=data.filter()

        if agn_sel !=None and agn_sel =="all":
            data=data
            print("in agn")

        if agn_sel !=None and agn_sel !="all":
            data=data.filter(agent=agn_sel)
            print("in agn2")


        if criteria_sel !="" and criteria_sel =="all":
            data=data
            print("in cri")
        # if criteria_sel != "" and criteria_sel !="all":
        #     data=data.filter()

        if fdate !="":
            print(data,'before')
            fdate = datetime.strptime(fdate,'%d-%m-%Y')
            tdate = datetime.strptime(tdate,'%d-%m-%Y')
            if fdate != tdate:
                tdate = tdate + timedelta(days=1)

            fdate = fdate.strftime("%Y-%m-%d")
            tdate = tdate.strftime("%Y-%m-%d")
            if fdate == tdate:
                data=data.filter(lastupdate__icontains=tdate)
            else:
                data=data.filter(lastupdate__range=[fdate,tdate])

        print(data,"datattaatata")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Agent Name","Direction","Phone No.","Sub disposition","Contacted DateTime","Recording fiile","marks1","got","marks2","got","marks3","got","marks4","got","marks5","got","marks6","got","marks7","got","marks8","got","marks9","got","Total","Got","Performance"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = data.values_list("agent","direction",'phone',"sub","contacted_dt","recordingfile","m1","gm1","m2","gm2","m3","gm3","m4","gm4","m5","gm5","m6","gm6","m7","gm7","m8","gm8","m9","gm9","total","got","performance")

        print("in rows")
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

    return JsonResponse({"status":400})
#//////////////////Quality Score card ends////////////////
