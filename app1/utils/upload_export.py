from ..views_imports import *


def convert_date(dt):
    try:
        dt = datetime.strptime(dt,'%Y-%m-%d').date()
    except Exception as e:
        # print(e)
        dt = None
    return dt

def upload_ajax(request):
    if request.method == "POST":
        list_id = request.POST.get('list_id')
        list_name = request.POST.get('list_name')
        excel_file = request.FILES.get('excel_file')
        
        # if list id already exists return error
        if Dataupload.objects.filter(list_id=list_id).exists():
            return JsonResponse({'status':300,"message":"List_id already exists"})

        try:
            df = pd.read_csv(excel_file) #reading excel file
            row_count = df.shape[0] #counting rows
            print(row_count)
            df.fillna("",inplace=True) #replacing nan with empty str
            #upload list details
            # Dataupload.objects.create(list_id=list_id,list_name=list_name,count=row_count,excel_file=excel_file)

            skipped_row = [] #skipped rows while uploading
            for i, row in df.iterrows():
                # print(row['EDI Start Date'],row['Closing Date'],row['Business Address Line 1'],"ASDASDyryjnieemeneownfoneoiehgh;ieurt")
                # # converting str to date
                # row['EDI Start Date'] = convert_date(row['EDI Start Date'])
                # row['Closing Date'] = convert_date(row['Closing Date'])
                print(i,row)


                # try:
                #     LeadDetails.objects.create(list_id=list_id)
                # except Exception as e:
                #     print(e)
                #     skipped_row.append(i+1)

            print(skipped_row)
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})

    return JsonResponse({'status':200})
