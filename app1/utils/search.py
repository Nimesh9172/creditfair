from ..views_imports import *


@login_required(login_url="login")
def searchajax(request):
    if request.method == 'POST':
        given_name=request.POST.get('name')
        given_phone=request.POST.get("mobile_number")
        given_loan=request.POST.get("agreement_no")
        if given_name == None or given_phone == None or given_loan == None:
            given_name = ""
            given_loan = ""
            given_phone = ""
        
        print(given_name,"asdasd")
        print(given_phone,"asdasd")
        print(given_loan,"asdasd")
        try:
            add = AdditionalInfo.objects.values_list('lead_id_id',flat=True).get(phone_no=given_phone)
            # print("in addddddddddddddddddddddddddddddddddddddddd",add)
        except:
            add = None
            if add == 0:
                add = None
        # print(add,"Additional")
        try:
            if request.user.user_level == 9:
                per=LeadDetails.objects
            else:
                per=LeadDetails.objects.filter(caller_name=request.user.username)
            
            if given_name != "":
                per=per.filter(name__icontains=given_name)

            elif given_phone != "":
                per=per.filter(Q(mobile_no__icontains=given_phone) | Q(id = add) | Q(additional_no__icontains=given_phone) | Q(co_mobile_no__icontains=given_phone))

            elif given_loan != "":
                per=per.filter(agreement_no__icontains=given_loan)

            if given_name  != "" or given_phone != "" or given_loan != "":
                per = per.exclude(list_forkey__status__icontains="0")[:100]
            #     per=LeadDetails.objects
            
            # print(per)
            return JsonResponse({"status":200,'all_data':list(per.values())})
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})
    
    return JsonResponse({'status':400})

@login_required(login_url="login")
def search(request):

    return render(request,"search/search.html")

