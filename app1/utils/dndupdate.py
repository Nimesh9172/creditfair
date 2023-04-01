from ..views_imports import *

@login_required(login_url="login")
def dnd_view(request):
    obj = dnd_upload.objects.all()
    return render(request,"dnd/dnd.html",{'obj':obj})

def uploadajax_dnd(request):
    dt=datetime.now()
    user=request.user.username
    data = LeadDetails.objects
    if request.method == "POST":
        excel_file = request.FILES.get('excel_file')
        print(excel_file,'filepath')
        try:
            df = pd.read_csv(excel_file) #reading excel file
            row_count = df.shape[0] #counting rows
            print(row_count)
            df.fillna("",inplace=True) #replacing nan with empty str
            #upload list details
            update_dnd_upload=dnd_upload.objects.create(entry=dt,count=row_count,file=excel_file,uploaded_by=user)
            skipped_row = [] #skipped rows while uploading
            for i, row in df.iterrows():
                print('excel datas',row['Mobile No.'],row['Reason'],row['End Date'])
                try:
                   update_dnd=data.filter(mobile_no=row['Mobile No.']).update(dnd_detail=1)
                   dataf = data.get(mobile_no=row['Mobile No.'])
                   dnd.objects.create(dnd_forid=update_dnd_upload,per_forid=dataf,reason=row['Reason'],enddate=row['End Date'])
                except Exception as e:
                    skipped_row.append(i+1)
                    msg=str(e)
                    print('exception',e)
            print(skipped_row)
        except Exception as e:
            print(e)
            msg=str(e)
            return JsonResponse({'status':300,"msg":msg})

    return JsonResponse({"status":200})