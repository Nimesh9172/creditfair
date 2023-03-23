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
def leadupdate(request):
    return render(request,"leadupdate/leadupdate.html")

@login_required(login_url="login")
def dnd(request):
    return render(request,"dnd/dnd.html")

@login_required(login_url="login")
def sms(request):
    return render(request,"sms/sms.html")



