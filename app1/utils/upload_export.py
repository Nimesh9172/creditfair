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
            obj = Dataupload.objects.create(listid=list_id,listname=list_name,count=row_count,file=excel_file)
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
                    LeadDetails.objects.create(agreement_no=row['Agreement Number'],agreement_id=row['Id'],name=row['Name'],co_name=row['Co Applicant Name'],co_mobile_no=row['Co Applicant Number'],merchant_name=row['Merchant  Name'],lender_name=row['Lender Name'],email=row['Email'],mobile_no=row['Phone'],main_amount=row['Amount'],first_emi_date=row['First EMI Date'],nach_status=row['Nach Status'],advisor=row['Advisor'],address=row['Current City'],state=row['Current State'],caller_name=row['Caller'],due_date=row['Due Date'],pincode=row['Pincode'],list_forkey=obj,list_id=list_id)
                except Exception as e:
                    print(e)
                    skipped_row.append(i+1)

            print(skipped_row)
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})

    return JsonResponse({'status':200})
