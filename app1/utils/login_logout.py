from ..views_imports import *
from .apr_views import *

def loginuser(request):
    return render(request,'login/login.html')

def login_user_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        extension = request.POST.get('extension')
        entry=datetime.now()

        if not User.objects.filter(username=username).exists():
            return JsonResponse({'status':301})

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            User.objects.filter(username=username).update(extension=extension,is_loggedin=1)
            LoginHistory.objects.create(username=username,logdt=entry,event="LOGIN")
            login_apr(request)
            # return redirect()
            return JsonResponse({'status':200})

        print(username,password,"isidipssss")
    return JsonResponse({"status":400})

@login_required(login_url='login')
def logoutuser(request):
    dt = datetime.now()
    User.objects.filter(username=request.user.username).update(is_loggedin=0)
    LoginHistory.objects.create(username=request.user.username,logdt=dt,event="LOGOUT")   
    logout_apr(request)
    logout(request)
    return redirect('login')
