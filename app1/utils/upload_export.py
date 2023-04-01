from ..views_imports import *

def convert_date(dt):
    try:
        dt = datetime.strptime(dt,'%Y-%m-%d').date()
    except Exception as e:
        # print(e)
        dt = None
    return dt

def check_list_id(request):
    query = Dataupload.objects.all()
    ser = DatauploadSerializer(query,many=True)
    return JsonResponse({"status":400,"list_id":ser.data})


def datastatus(request):
    if request.method=="POST":
        an=request.POST.get("an")
        lstid=request.POST.get("lstid")
        print(an,lstid)
        Dataupload.objects.filter(id=lstid).update(status=an)
        print("info",an,lstid,Dataupload.objects.filter(id=lstid))
    return JsonResponse({'status':400})

@login_required(login_url="login")
def upload_export(request):
    obj = Dataupload.objects.all().order_by('-id')
    return render(request,"upload_export/upload_export.html",{"obj":obj})

def upload_ajax(request):
    user=request.user.username
    if request.method == "POST":
        list_id = request.POST.get('list_id')
        list_name = request.POST.get('list_name')
        excel_file = request.FILES.get('excel_file')
        
        print(list_id,list_name,excel_file)

        # if list id already exists return error
        if list_id == "":
            return JsonResponse({'status':300,"message":"Enter List Id"})

        if Dataupload.objects.filter(listid=list_id).exists():
            return JsonResponse({'status':300,"message":"List_id already exists"})

        try:
            df = pd.read_csv(excel_file,encoding='utf-16') #reading excel file
            row_count = df.shape[0] #counting rows
            print(row_count,"rowwww counttt")
            df.fillna("",inplace=True) #replacing nan with empty str
            #upload list details
            obj = Dataupload.objects.create(listid=list_id,listname=list_name,count=row_count,file=excel_file,uploaded_by=user)
            obj.save()
            skipped_row = [] #skipped rows while uploading
            for i, row in df.iterrows():
                if len(str(row['Id'])) < 1 and len(row['Agreement Number']) < 1:
                    print("empttttt") 
                    Dataupload.objects.get(id=obj.id).delete()
                    break
            
                # converting str to date
                row['First EMI Date'] = convert_date(row['First EMI Date'])
                row['Due Date'] = convert_date(row['Due Date'])

                try:
                    LeadDetails.objects.create(agreement_no=row['Agreement Number'],agreement_id=row['Id'],name=row['Name'],co_name=row['Co Applicant Name'],co_mobile_no=row['Co Applicant Number'],merchant_name=row['Merchant  Name'],lender_name=row['Lender Name'],email=row['Email'],mobile_no=row['Phone'],main_amount=row['Amount'],first_emi_date=row['First EMI Date'],nach_status=row['Nach Status'],advisor=row['Advisor'],address=row['Current City'],state=row['Current State'],caller_name=row['Caller'],uploaded_by=user,due_date=row['Due Date'],pincode=row['Pincode'],list_forkey=obj,list_id=list_id)
                except Exception as e:
                    print(e)
                    skipped_row.append(i+1)

            print(skipped_row)
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})

    return JsonResponse({'status':200})


def dataexport(request):
    read=LogData.objects
    if request.method == "POST":
        sd = request.POST.get('fdate')
        ed = request.POST.get('todate')
        # sel = request.POST.getlist('remcb')
        agn = request.POST.get('agn')
        sel=request.POST.get("sel")
        apr=request.POST.get("apr")

        print(sd,ed,sel,apr)
        print(sel,sd,ed)
        if sd != "" and ed != "":
            sd = datetime.strptime(sd,'%d-%m-%Y')
            ed= datetime.strptime(ed,'%d-%m-%Y')
            ed = ed + timedelta(days=1)
            sd= sd.strftime("%Y-%m-%d")
            ed= ed.strftime("%Y-%m-%d")
            read=read.filter(contacted_dt__range=[sd,ed])

        if  sel != None and sel != "":
            print(sel,"inside if")
            read=read.filter(sub_disposition=sel)
            print(read)

        if  agn != None and agn != "":
            print(agn,"inside if")
            read=read.filter(caller_name=agn)
            print(read)
        
        print("YOUR FINAL REPORT",read)
        
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data') 

            row_num = 0

            columns = ["Name","Mobile no","Address","State","Pincode","email","Co Applicant Name","Co Applicant Number","lender Name","Merchant Name","Agreement ID","Agreement No.","Due Date","NACH Status","Advisor","Amount","First EMI Amount","Reference Name1","Reference No1","Reference Name2","Reference No2","Additional Address","Additional Email","Additional No.","Last Dial No","Caller Name","Disposition","Sub Disposition","Contacted Datetime","AHT","Callback Time","Collected Amount","Mode of Payment","Transaction No.","Remark"]

            rows =  read.values_list("name","mobile_no","address","state","pincode","email","co_name","co_mobile_no","lender_name","merchant_name","agreement_id","agreement_no","due_date","nach_status","advisor","main_amount","first_emi_date","ref_name1","ref_no1","ref_name2","ref_no2","additional_address","additional_email","additional_no","last_dial_no","caller_name","disposition","sub_disposition","contacted_dt","AHT","callback_datetime","amount","mode_of_payment","cheque_transaction_no","remark")
            
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

            # Sheet body, remaining rows
            
         
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                  
                    data=str(row[col_num]).replace("nan"," ")
                    data=data.replace("None"," " )
                    if col_num == 30:
                        data = str(row[col_num])[:19]
                        print(col_num,str(row[col_num])[:19] )
                    ws.write(row_num, col_num,data)
            wb.save(response)

            return response

        except Exception as e:
            print(e)
    return JsonResponse({"status":200})
