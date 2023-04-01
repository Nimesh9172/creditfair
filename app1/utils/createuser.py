from .. views_imports import *

# ////////////////////create user views starts////////////////////

def createuser(request):
    userdata=User.objects.filter(Q(user_level=1) )
    for i in userdata:
        print(i.id,"iddddddddddddddddddddddddddddddddddddddddddddddd")
    return render(request,'creatuser/creatuser.html' ,{'userdata':userdata})

# @csrf_exempt
def savedata(request): 
    if request.method=="POST":
            print("its posted all")
            name=request.POST.get("name")
            print(name)
            passw=request.POST.get("password")
            print(passw)
            j_date=request.POST.get("joindate")
            
            query=User.objects.filter(user_level='1').last()
            
            if query:
                prev_user_id= query.username
            else:
                prev_user_id="CRF000"
                

            i=int(prev_user_id[3:])+1
            newid = f"CRF{i:03}" 
            print(newid)
           
            print(name,passw,j_date)
            # query=usercreatee.objects.filter("")

            User.objects.create_user(first_name=name,password=passw,display_pass=passw,date_joined=j_date,user_level='1',user_created_by=request.user.username,username=newid,status="1")

            stud=User.objects.values()
            # print(stud)
            dataa=list(stud)
            return JsonResponse({'status':'save','dataa':dataa,'idd':newid})
    else:
        return JsonResponse({'status':0})



def deletepost(request):
    if request.method=="POST":
        print('in status post')
        l_id=request.POST.get("lstid")
        status=request.POST.get("an")
        # dele=usercreatee.objects.filter(l_id=l_id).update(status="deleted")
        print('status',l_id,status)
        User.objects.filter(id=l_id).update(status=status)
        

        
        return JsonResponse({'status':'save'})

    else:
        return JsonResponse({'status':0})

    




def updateuser(request):
    #  data=usercreatee.objects.filter(pk=pk)
    id=0
    if request.method == "POST":
        id=request.POST.get("id")
        print('posted in update user',id)
        username=request.POST.get('userrname')
        print('userrrrrrrrrrrr',username)
        password=request.POST.get('userpass')


        if username != "":
            User.objects.filter(id=id).update(first_name=username)
        if password != "":
            us  = User.objects.get(id=id)
            us.display_pass = password
            us.set_password(password)
            us.save()

            return JsonResponse({'status':'save'})

    else:
        return JsonResponse({'status':0})


def search_in_table(request):
    data=User.objects.filter(id=id)
    if request.method =="POST":
        uid=request.POST.get("n_id")
        search=request.POST.get("search")

        return JsonResponse({'data':'data'})


# ////////////////////create user views starts////////////////////
