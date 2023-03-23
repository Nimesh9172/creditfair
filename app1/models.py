from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    user_level=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=25,null=True,blank=True)
    is_loggedin = models.CharField(max_length=2,null=True,blank=True,default=0)
    extension = models.CharField(max_length=10,null=True,blank=True)
    display_pass = models.CharField(max_length=50,null=True,blank=True)    

class LoginHistory(models.Model):
    username=models.CharField(max_length=100,null=True,blank=True)
    logdt=models.DateTimeField(null=True,blank=True)
    event = models.CharField(max_length=100,null=True,blank=True)

class Dataupload(models.Model):
    listid=models.CharField(max_length=100,null=True,blank=True,unique=True)
    listname=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(upload_to='uploaded_csv/',blank=True,null=True)
    count = models.BigIntegerField(null=True,blank=True)
    entry=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status=models.IntegerField(null=True,blank=True,default=1)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)

class LeadDetails(models.Model):
    #customer_info
    name = models.CharField(max_length=200,null=True,blank=True)
    mobile_no = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    co_name = models.CharField(max_length=200,null=True,blank=True)
    co_mobile_no = models.CharField(max_length=15,null=True,blank=True)

    #process_info
    lender_name = models.CharField(max_length=200,null=True,blank=True)
    merchant_name = models.CharField(max_length=200,null=True,blank=True)
    agreement_id = models.CharField(max_length=50,null=True,blank=True)
    agreement_no = models.CharField(max_length=100,null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)
    nach_status = models.CharField(max_length=200,null=True,blank=True)
    advisor = models.CharField(max_length=200,null=True,blank=True)

    #process Additional Info
    main_amount = models.CharField(max_length=100,null=True,blank=True)
    first_emi_date = models.DateField(null=True,blank=True)

    #Reference details or mortgage details
    ref_name1 = models.CharField(max_length=200,null=True,blank=True)
    ref_no1 = models.CharField(max_length=15,null=True,blank=True)
    ref_name2 = models.CharField(max_length=200,null=True,blank=True)
    ref_no2 = models.CharField(max_length=15,null=True,blank=True)

    
    #additional added during call for export data
    additional_address = models.TextField(null=True,blank=True)
    additional_email = models.CharField(max_length=150,null=True,blank=True)
    additional_no = models.CharField(max_length=15,null=True,blank=True)

    # agent captured details
    disposition = models.CharField(max_length=30,null=True,blank=True)
    sub_disposition = models.CharField(max_length=200,null=True,blank=True)
    callback_datetime = models.DateTimeField(null=True,blank=True)

    amount = models.CharField(max_length=30,null=True,blank=True)
    mode_of_payment = models.CharField(max_length=20,null=True,blank=True)
    cheque_transaction_no = models.CharField(max_length=100,null=True,blank=True)

    # system capture details
    contacted_dt = models.DateTimeField(auto_now=True,blank=True,null=True)
    attempted = models.BigIntegerField(null=True,blank=True) 
    caller_name = models.CharField(max_length=100,null=True,blank=True)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
    last_dial_no = models.CharField(max_length=15,null=True,blank=True)
    list_forkey = models.ForeignKey(Dataupload,on_delete=models.CASCADE,null=True,blank=True)
    list_id = models.CharField(max_length=200,null=True,blank=True)


class LogData(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    mobile_no = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    co_name = models.CharField(max_length=200,null=True,blank=True)
    co_mobile_no = models.CharField(max_length=15,null=True,blank=True)

    #process_info
    lender_name = models.CharField(max_length=200,null=True,blank=True)
    merchant_name = models.CharField(max_length=200,null=True,blank=True)
    agreement_id = models.CharField(max_length=50,null=True,blank=True)
    agreement_no = models.CharField(max_length=100,null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)
    nach_status = models.CharField(max_length=200,null=True,blank=True)
    advisor = models.CharField(max_length=200,null=True,blank=True)

    #process Additional Info
    main_amount = models.CharField(max_length=100,null=True,blank=True)
    first_emi_date = models.DateField(null=True,blank=True)

    #Reference details or mortgage details
    ref_name1 = models.CharField(max_length=200,null=True,blank=True)
    ref_no1 = models.CharField(max_length=15,null=True,blank=True)
    ref_name2 = models.CharField(max_length=200,null=True,blank=True)
    ref_no2 = models.CharField(max_length=15,null=True,blank=True)

    
    #additional added during call for export data
    additional_address = models.TextField(null=True,blank=True)
    additional_email = models.CharField(max_length=150,null=True,blank=True)
    additional_no = models.CharField(max_length=15,null=True,blank=True)

    # agent captured details
    disposition = models.CharField(max_length=30,null=True,blank=True)
    sub_disposition = models.CharField(max_length=200,null=True,blank=True)
    callback_datetime = models.DateTimeField(null=True,blank=True)

    amount = models.CharField(max_length=30,null=True,blank=True)
    mode_of_payment = models.CharField(max_length=20,null=True,blank=True)
    cheque_transaction_no = models.CharField(max_length=100,null=True,blank=True)

    # system capture details
    contacted_dt = models.DateTimeField(auto_now=True,blank=True,null=True)
    attempted = models.BigIntegerField(null=True,blank=True) 
    caller_name = models.CharField(max_length=100,null=True,blank=True)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
    last_dial_no = models.CharField(max_length=15,null=True,blank=True)
    list_forkey = models.CharField(max_length=30,null=True,blank=True)
    list_id = models.CharField(max_length=200,null=True,blank=True)

class AdditionalInfo(models.Model):
    email = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    phone_no = models.CharField(max_length=15,null=True,blank=True)
    whatsapp_no = models.CharField(max_length=15,null=True,blank=True)
    lead_id = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True,blank=True)