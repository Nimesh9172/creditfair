from ..views_imports import *

@login_required(login_url="login")
def leadupdate(request):
    obj = Leadupload.objects.all()
    return render(request,"leadupdate/leadupdate.html",{'obj':obj})

def check_list_id_leadupdate(request):
    query = Leadupload.objects.all()
    # print("check_list_id")
    ser = LeaduploadSerializer(query,many=True)
    # print("after",ser)
    return JsonResponse({"status":400,"list_id":ser.data})

def uploadajax_lead(request):
    dt=datetime.now()
    user=request.user.username
    data = LeadDetails.objects
    if request.method == "POST":
        list_id = request.POST.get('list_id')
        list_name = request.POST.get('list_name')
        excel_file = request.FILES.get('excel_file')
        print(excel_file,'filepath')
        if list_id == "":
            return JsonResponse({'status':300,"message":"Enter List Id"})

        if Leadupload.objects.filter(listid=list_id).exists():
            return JsonResponse({'status':300,"message":"List_id already exists"})
        try:
            df = pd.read_csv(excel_file) #reading excel file
            row_count = df.shape[0] #counting rows
            print(row_count)
            df.fillna("",inplace=True) #replacing nan with empty str
            #upload list details
            Leadupload.objects.create(listid=list_id,listname=list_name,count=row_count,file=excel_file,uploaded_by=user)
            skipped_row = [] #skipped rows while uploading
            for i, row in df.iterrows():
                try:
                    # data.filter(agreement_no=row['Agreement Number']).update(name=row['Name'],mobile_no=row['Mobile No.'],address=row['Address'],main_amount=row['Amount'],caller_name=row['Caller Name'])
                    print(row['Name'],row['Mobile No.'],row['Address'],row['Amount'],row['Caller Name'])
                    if row['Name'] != '':
                        data.filter(agreement_no=row['Agreement Number']).update(name=row['Name'])
                    if row['Mobile No.'] != '':
                        data.filter(agreement_no=row['Agreement Number']).update(mobile_no=row['Mobile No.'])
                    if row['Address'] != '':
                        data.filter(agreement_no=row['Agreement Number']).update(address=row['Address'])
                    if row['Amount'] != '':
                        data.filter(agreement_no=row['Agreement Number']).update(main_amount=row['Amount'])
                    if row['Caller Name'] != '':
                        data.filter(agreement_no=row['Agreement Number']).update(caller_name=row['Caller Name'])
                except Exception as e:
                    skipped_row.append(i+1)
                    msg=str(e)
                    print(e)
            print(skipped_row)
        except Exception as e:
            print(e)
            msg=str(e)
            return JsonResponse({'status':300,"msg":msg})
    return JsonResponse({"status":200})
