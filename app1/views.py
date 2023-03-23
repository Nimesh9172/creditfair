from .views_imports import *

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'base.html')

def loginuser(request):
    return render(request,'login/login.html')

def login_user_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        campaigns = request.POST.get('campaign_sel')
        entry=datetime.now()

        if not User.objects.filter(username=username).exists():
            return JsonResponse({'status':301})

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            LoginHistory.objects.create(username=username,logdt=entry,event="LOGIN")
            return JsonResponse({'status':200})

        print(username,password,"isidipssss")
    return JsonResponse({"status":400})


@login_required(login_url='login')
def logoutuser(request):
    dt = datetime.now()
    LoginHistory.objects.create(username=request.user.username,logdt=dt,event="LOGOUT")   
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def searchajax(request):
    # if request.method == 'POST':
    #     given_name=request.POST.get('borrowor_name')
    #     given_phone=request.POST.get("mobile_number")
    #     given_loan=request.POST.get("loan_id")
    #     print(given_name)
    #     print(given_phone)
    #     print(given_loan)
    #     if given_name == None or given_phone == None or given_loan == None:
    #         given_name = ""
    #         given_loan = ""
    #         given_phone = ""
        
    #     try:
    #         add = Additional.objects.values_list('debtor_id',flat=True).get(contactnum=given_phone)
    #     except:
    #         add = None
    #         if add == 0:
    #             add = None
    #     try:
    #         if request.user.user_level == 9:
    #             per=personaldetails.objects
    #         else:
    #             per=personaldetails.objects.filter(callername=request.user.username).exclude(list_id__status__contains="0")
            
    #         if given_name != "":
    #             per=per.filter(borrowor_name__icontains=given_name).exclude(list_id__status__contains="0")
    #         elif given_phone != "":
    #             per=per.filter(Q(mobile_number__icontains=given_phone) | Q(id = add) | Q(alt_mno_1__icontains=given_phone) | Q(alt_mno_2__icontains=given_phone)  | Q(alt_mno_3__icontains=given_phone)).exclude(list_id__status__contains="0")
    #         elif given_loan != "":
    #             per=per.filter(bank_loan_accountno__icontains=given_loan).exclude(list_id__status__contains="0")

    #         if given_name  == "" and given_phone == "" and given_loan == "":
    #             per=personaldetails.objects.filter(id__isnull=True).exclude(list_id__status__contains="0")
            
    #         per = per[:100]
     
    #         return JsonResponse({"status":200,'all_data':list(per.values())})
    #     except Exception as e:
    #         print(e)
    #         return JsonResponse({'status':300})

    
    return JsonResponse({'status':400})

@login_required(login_url="login")
def search(request):
    return render(request,"search/search.html")

@login_required(login_url="login")
def reminder(request):
    return render(request,"reminder/reminder.html")

@login_required(login_url="login")
def recovery(request):
    return render(request,"recovery/recovery.html")

@login_required(login_url="login")
def missedcall(request):
    return render(request,"missedcall/missedcall.html")

@login_required(login_url="login")
def ots(request):
    return render(request,"ots/ots.html")

@login_required(login_url="login")
def non_attempted(request):
    return render(request,"non_attempted/non_attempted.html")

@login_required(login_url="login")
def connect_to_customer(request):
    return render(request,"connect_to_customer/connect_to_customer.html")

@login_required(login_url="login")
def upload_export(request):
    return render(request,"upload_export/upload_export.html")

@login_required(login_url="login")
def leadupdate(request):
    return render(request,"leadupdate/leadupdate.html")

@login_required(login_url="login")
def dnd(request):
    return render(request,"dnd/dnd.html")

@login_required(login_url="login")
def sms(request):
    return render(request,"sms/sms.html")



