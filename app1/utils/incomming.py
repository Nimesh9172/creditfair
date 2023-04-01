from .. views_imports import *

def inc_cms(request):
    lead__id = request.GET.get('id')
    rendered = request.GET.get('render')
    try:
        obj = LeadDetails.objects.get(id=lead__id)
        context = {'id':lead__id,'name':obj.name,'mobile':obj.mobile_no,'address':obj.address,'state':obj.state,'pincode':obj.pincode,'email':obj.email,'co_name':obj.co_name,'co_mobile_no':obj.co_mobile_no,'lender_name':obj.lender_name,'merchant_name':obj.merchant_name,'agreement_id':obj.agreement_id,'agreement_no':obj.agreement_no,'due_date':obj.due_date,"nach_status":obj.nach_status,"advisor":obj.advisor,'amount':obj.main_amount,'first_emi_date':obj.first_emi_date,'caller_name':obj.caller_name,"sub_disposition":obj.sub_disposition,"contacted_dt":obj.contacted_dt,'remark':obj.remark,'render':rendered,'last_dial':obj.last_dial_no}
    except Exception as e:
        print(e)
        context={}
    return render(request,'incomming/incomming.html',context)

def updatefield(request):
    data=LeadDetails.objects
    if request.method == 'POST':
        name_val = request.POST.get('name_val') # will get the name of input 
        update_val = request.POST.get('update_val') # will get the name of input 
        id = request.POST.get('id') # will get the id of input 
        print(update_val,name_val,'testingggg')
        if name_val == 'name' and update_val != '':
            data=data.filter(id=id).update(name=update_val)
        if name_val == 'edit_address' and update_val != '':
            data=data.filter(id=id).update(address=update_val)
        if name_val == 'state' and update_val != '':
            data=data.filter(id=id).update(state=update_val)
        if name_val == 'pincode' and update_val != '':
            data=data.filter(id=id).update(pincode=update_val)
        if name_val == 'edit_email' and update_val != '':
            data=data.filter(id=id).update(email=update_val)
        if name_val == 'co_name' and update_val != '':
            data=data.filter(id=id).update(co_name=update_val)
        if name_val == 'co_mobile_no' and update_val != '':
            data=data.filter(id=id).update(co_mobile_no=update_val)
        if name_val == 'lender_name' and update_val != '':
            data=data.filter(id=id).update(lender_name=update_val)
        if name_val == 'merchant_name' and update_val != '':
            data=data.filter(id=id).update(merchant_name=update_val)
        if name_val == 'agreement_id' and update_val != '':
            data=data.filter(id=id).update(agreement_id=update_val)
        if name_val == 'agreement_no' and update_val != '':
            data=data.filter(id=id).update(agreement_no=update_val)
        if name_val == 'due_date' and update_val != '':
            data=data.filter(id=id).update(due_date=update_val)
        if name_val == 'nach_status' and update_val != '':
            data=data.filter(id=id).update(nach_status=update_val)
        if name_val == 'advisor' and update_val != '':
            data=data.filter(id=id).update(advisor=update_val)
        if name_val == 'amount' and update_val != '':
            data=data.filter(id=id).update(amount=update_val)
        if name_val == 'firstemidate' and update_val != '':
            data=data.filter(id=id).update(first_emi_date=update_val)   
        
        print(data,'data')
            
    return JsonResponse({'status':200})




def incoming_search_ajax(request):
    if request.method == 'POST':
        given_name=request.POST.get('search')
      
        print(given_name)
        if given_name == None:
            given_name = ""
       
        try:
            if request.user.user_level == 9:
                per=LeadDetails.objects
            else:
                per=LeadDetails.objects.filter(callername=request.user.username)
            
            print(request.user.user_level,"lelevlevl")
            if len(given_name) > 0:
                per=per.filter(Q(mobile_no__icontains=given_name) | Q(name__icontains = given_name)|Q(agreement_no__icontains=given_name))
            
            
            # per = per[:100]
            print(per)
     
            return JsonResponse({"status":200,'all_data':list(per.values())})
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})

    return JsonResponse({'status':400})

def card1update(request):
    id=''
    if request.method=='POST':
        id = request.POST.get('id')
        print(id,'from json')
    card1=LeadDetails.objects.filter(id=id)
    history_data=LogData.objects.filter(lead_forkey=id)
    if len(history_data) == 0:
        print("inside if")
        show=False
    else:
        print("else")
        show=True
    print(card1)
    # print(history_data,'logdata',show)
    return JsonResponse({"status":200,"card1":list(card1.values()),"history_data":list(history_data.values()),"show":show})

def additional_update(request):
    id = ''
    if request.method=="POST":
        id = request.POST.get('id')
        data = AdditionalInfo.objects.filter(lead_id=id)
    return JsonResponse({'status':200,"data":list(data.values())})


def check_for_incoming(request):
    dt=datetime.now().date()
    info=Incoming_info.objects.filter(called=request.user.extension).last()
    print(info,"inbounddddddddddd")
    if info:
        print("info.status",info.status  )
        if info.status == "Answered" and info.status !="attend_transfer":
            ph=info.caller
            if ph.startswith("+91"):
                ph=ph[3:]
            mb=info.caller
            print("phhhhhhhhhhhhhhhhh",ph)
            per=LeadDetails.objects.filter(mobile_no=ph)
            if per:
                info=Incoming_info.objects.filter(caller=mb).update(status="PickUp")
                print("before bcz its present")
                per=LeadDetails.objects.filter(Q(mobile_no=ph)|Q(additional_no=ph)).last()
                per=per.id

                return JsonResponse({"status":400,'id':per})
            else:
                info=Incoming_info.objects.filter(caller=mb).update(status="PickUp")
                # info=Live_incoming.objects.filter(extension=request.user.extension).update(status="PickUp")
                per=LeadDetails.objects.create(mobile_no=ph,created_by="Inbound")
                per.save()
                print("in else")
               
                
                per = per.id


            return JsonResponse({"status":400,"id":per})
    print(info)
    return JsonResponse({"status":200})



