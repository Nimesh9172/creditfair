from ..views_imports import *
from .apr_views import *

def cms(request):
    lead__id = request.GET.get('id')
    rendered = request.GET.get('render')
    progressive = request.GET.get('progressive')
    try:
        obj = LeadDetails.objects.get(id=lead__id)
        context = {'id':lead__id,'name':obj.name,'mobile':obj.mobile_no,'address':obj.address,'state':obj.state,'pincode':obj.pincode,'email':obj.email,'co_name':obj.co_name,'co_mobile_no':obj.co_mobile_no,'lender_name':obj.lender_name,'merchant_name':obj.merchant_name,'agreement_id':obj.agreement_id,'agreement_no':obj.agreement_no,'due_date':obj.due_date,"nach_status":obj.nach_status,"advisor":obj.advisor,'amount':obj.main_amount,'first_emi_date':obj.first_emi_date,'caller_name':obj.caller_name,"sub_disposition":obj.sub_disposition,"contacted_dt":obj.contacted_dt,'remark':obj.remark,'render':rendered,'last_dial':obj.last_dial_no}
    except Exception as e:
        print(e)
        context={}
    context['progressive'] = progressive
    return render(request,'cms/cms.html',context)

def addition_details_ajax(request):
    if request.method == "POST":
        id = request.POST.get('id')
        contact_no = request.POST.get('contact_no') 
        address = request.POST.get('address') 
        email = request.POST.get('email') 
        wap_no = request.POST.get('wap_no') 
        wap_no_inp = request.POST.get('wap_no_inp') 
        relation = request.POST.get('relation')
        print(contact_no,"contactnoooo",address,"adress",email,"emaillll",wap_no,"wap_nooooo",wap_no_inp,"wap_no_inp",relation,"ssdfds",id)

        try:
            lead_instance= LeadDetails.objects.get(id=id)
        except Exception as e:
            return JsonResponse({'status':300})
        


        if len(contact_no) > 6:
            AdditionalInfo.objects.create(lead_id=lead_instance,relation=relation,phone_no=contact_no)
        
        if address != "" and len(address) >= 1:
            AdditionalInfo.objects.create(lead_id=lead_instance,address=address)

        if wap_no != "add_no" and len(wap_no) > 7:
            AdditionalInfo.objects.create(lead_id=lead_instance,whatsapp_no=wap_no)

        if len(wap_no_inp) > 4:
            AdditionalInfo.objects.create(lead_id=lead_instance,whatsapp_no=wap_no_inp)

        if len(email) > 5:
            AdditionalInfo.objects.create(lead_id=lead_instance,email=email)

            

    return JsonResponse({'status':200})


def get_additional_info(request):
    lead_id = request.GET.get("id")
    try:
        obj = AdditionalInfo.objects.filter(lead_id=lead_id)
        obj = AdditionalInfoSerializer(obj,many=True)
    except Exception as e:
        print(e)
        return JsonResponse({"status":300,"data":"No data found"})

    return JsonResponse({"status":200,"data":obj.data})

def cms_submit_ajax(request):
    if request.method == "POST":
        data = {k: None if v == 'undefined' else v for k, v in request.POST.items()}
        lead_id = data.get('lead_id')
        dispo = data.get('dispo')
        subdispo = data.get('subdispo')
        remark = data.get('remark')
        ptp_date = data.get('ptp_date')
        ptp_amount = data.get('ptp_amount')
        callback_time = data.get('callback_time')
        schdatetime = data.get('schdatetime')
        ots_amount = data.get('ots_amount')
        paid_amt = data.get('paid_amt')
        mode = data.get('mode')
        cheque_no = data.get('cheque_no') 
        online = data.get('online')
        lastdial = data.get('lastdial')

        username = request.user.username
        ext = request.user.extension

        current_date = datetime.now().date()

        if lastdial:
            lastdial = lastdial[:10]

        try:
            obj = LeadDetails.objects.get(id=lead_id)
            print(obj)
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})

        if not dispo or not subdispo:
            return JsonResponse({'status':300})

        obj.disposition = dispo
        obj.sub_disposition = subdispo
        obj.remark = remark
        obj.attempted =  obj.attempted + 1
        obj.caller_name = request.user.username
        obj.direction = "Out"

        dt = datetime.now()
        am = dt + timedelta(minutes=0)

        # print(type(am))

        ft= am.strftime("%Y-%m-%d %H:%M:%S")

        if callback_time == "15min":
            am = dt + timedelta(minutes=15)
        elif callback_time == "30min":
            am = dt + timedelta(minutes=30)
        elif callback_time == "45min":
            am = dt + timedelta(minutes=45)
        elif callback_time == "60min":
            am = dt + timedelta(minutes=60)


        if callback_time:

            obj.callback_datetime = am
        elif ptp_date:
            obj.callback_datetime = ptp_date
        else :
            obj.callback_datetime = schdatetime
        
        if ptp_amount:
            obj.amount = ptp_amount
        elif paid_amt:
            obj.amount = paid_amt
        elif ots_amount:
            obj.amount = ots_amount

        obj.mode_of_payment = mode

        if cheque_no:
            obj.cheque_transaction_no = cheque_no
        else:
            obj.cheque_transaction_no = online

        if lastdial:
            obj.last_dial_no = lastdial


        obj.save()
        

        if dispo and lastdial:
            call_to = lastdial
        else:
            call_to = obj.mobile_no

        agid = agentevents.objects.filter(call_time__icontains=current_date,personalkey=obj.id,call_from=request.user.extension,call_to=call_to).last()
        print(agid)
        if agid:
            agentevents.objects.filter(id=agid.id).update(disposed_time=dt)
        
        dispose_apr(request,obj.id)

        LogData.objects.create(name=obj.name,mobile_no=obj.mobile_no,address=obj.address,state=obj.state,pincode=obj.pincode,email=obj.email,co_name=obj.co_name,co_mobile_no=obj.co_mobile_no,lender_name=obj.lender_name,merchant_name=obj.merchant_name,agreement_id=obj.agreement_id,agreement_no=obj.agreement_no,nach_status=obj.nach_status,due_date=obj.due_date,advisor=obj.advisor,main_amount=obj.main_amount,first_emi_date=obj.first_emi_date,ref_name1=obj.ref_name1,ref_no1=obj.ref_no1,ref_name2=obj.ref_name2,ref_no2=obj.ref_no2,additional_email=obj.additional_email,additional_address=obj.additional_address,additional_no=obj.additional_no,disposition=obj.disposition,sub_disposition=obj.sub_disposition,callback_datetime=obj.callback_datetime,remark=obj.remark,amount=obj.amount,mode_of_payment=obj.mode_of_payment,cheque_transaction_no=obj.cheque_transaction_no,contacted_dt=obj.contacted_dt,attempted = obj.attempted,caller_name=obj.caller_name,uploaded_by=obj.uploaded_by,last_dial_no=obj.last_dial_no,list_id=obj.list_id,lead_forkey=obj,dnd_detail=obj.dnd_detail,direction=obj.direction)

        cdr_update_dispositions(subdispo,ext,username,lead_id)
        if ptpbehaviour.objects.filter(forkey=obj.id).exists() != True:

            if obj.sub_disposition == "Promise To Pay":
                pt_pquery = ptpbehaviour.objects.create(first_status=obj.sub_disposition,first_date=obj.callback_datetime,forkey_id=obj.id,callerid=obj.caller_name,first_contact_datetime=obj.contacted_dt,main_amount=obj.main_amount,agreement_no=obj.agreement_no,lender_name=obj.lender_name,name=obj.name,ptp_amount=obj.amount )
                pt_pquery.save()

        else :
            if ptpbehaviour.objects.filter(forkey=obj.id).filter(first_status="Promise To Pay").exists() and obj.sub_disposition == "Promise To Pay":
                ptpbehaviour.objects.update(first_status=obj.sub_disposition,first_date=obj.callback_datetime,first_contact_datetime=obj.contacted_dt,next_status=None,next_date=None,next_contact_datetime=None)
            else:
                ptpbehaviour.objects.filter(forkey=obj.id).update(next_status=obj.sub_disposition,next_date=obj.callback_datetime,next_contact_datetime=obj.contacted_dt)
    
        return JsonResponse({'status':200})

    return JsonResponse({'status':300})

def get_additional_numbers(request):
    lead_id = request.GET.get('id')

    obj = AdditionalInfo.objects.filter(lead_id=lead_id)
    obj2 = LeadDetails.objects.filter(id=lead_id)
    ser2 = LeadDetailsSerializer(obj2,many=True)
    ser = AllNumbersSerializers(obj,many=True)
    return JsonResponse({"status":200,"data":ser.data,"data2":ser2.data})


def customer_history(request):
    lead_id = request.GET.get("id")
    obj = LogData.objects.filter(lead_forkey=lead_id).order_by('-id')[:10]
    ser = HistorySerializers(obj,many=True)

    return JsonResponse({"status":200,"data":ser.data})



