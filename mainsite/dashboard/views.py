import json
from django.shortcuts import render
import requests
from requests.api import request
from .userclass import Administrator_User, Standard_User
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date
import datetime
import time


#authorize api and get access token
def getAccessToken():
    strPassword ='password'
    payload = {'client_id':client_id,'client_secret':client_secret,'username':auth_id,'password':auth_secret,'grant_type':strPassword}
    response = requests.post("https://api.dubber.net/"+region+"/v1/token", params=payload)
    return response

def getDubPoints():
    payload ={'count': '100'}
    response = requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/dub_points", headers={"Authorization":"Bearer "+access_token},params= payload)
    return response  

def getAccountInfo():
    response = requests.get("https://api.dubber.net/"+region+"/v1/profile",headers={"Authorization":"Bearer "+access_token})
    return response 

def getAdminUsers():
    payload ={'role': 'Administrator','count':'100'}
    response = requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/users", headers={"Authorization":"Bearer "+access_token},params= payload)
    return response  

def getStandardUsers():
    payload ={'role': 'Standard%20User','count':'100'}
    response = requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/users", headers={"Authorization":"Bearer "+access_token},params= payload)
    return response  

def get_csv_dwnld_link(from_date,to_date):
    body_data = {'from_date':from_date,
            'to_date':to_date}
            #
    response = requests.post("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/data_exports", headers={"Authorization":"Bearer "+access_token,"Content-Type":"application/json","X-Date-Format":"ISO8601"},data= json.dumps(body_data) )
    #time.sleep(30)
    return response

# Create your views here.
def home(request):
    return render(request,'dashboard/api_login.html')

def account_info(request):
        response = getAccountInfo()
        account_json = response.json()
        return render(request,'dashboard/account_info.html',{'account_json':account_json,'page_name':'Account Information'})

def api_token_info(request):
    return render(request,'dashboard/api_token_info.html',{'access_token':access_token,'token_expiry':token_expiry,'refresh_token':refresh_token,'user_context':user_context})

def api_login(request):
    if request.method == 'POST':
        global region
        region = request.POST.get('region')
        global account_id
        account_id = request.POST.get('account_id')
        global auth_id 
        auth_id = request.POST.get('auth_id')
        global auth_secret
        auth_secret = request.POST.get('auth_secret')
        global client_id 
        client_id = request.POST.get('client_id')
        global client_secret
        client_secret = request.POST.get('client_secret')
        global accessToken

        request.session['region'] = region
        request.session['auth_id'] = auth_id
        request.session['auth_secret'] = auth_secret
        request.session['client_id'] = client_id
        request.session['client_secret'] = client_secret
        request.session['account_id'] = client_secret
        response = getAccessToken()
        if response.ok == True:
             json_response = response.json()
             global access_token, token_expiry , refresh_token ,user_context
             access_token = str(json_response["access_token"])
             token_expiry = int(json_response["expires_in"])
             refresh_token = str(json_response["refresh_token"])
             user_context = str(json_response["user_context"])

             request.session['access_token'] = access_token
             request.session['token_expiry'] = token_expiry
             request.session['refresh_token'] = refresh_token
             request.session['user_context'] = user_context
             return render(request,'dashboard/api_token_info.html',{'access_token':access_token,'token_expiry':token_expiry,'refresh_token':refresh_token,'user_context':user_context,'page_name':'API Token Information'})
        else:
            error_msg = response.text
            posted_url = response.url
            return render(request,'dashboard/api_login_failed.html',{'error_msg':error_msg,'posted_url':posted_url})

    else:
         return render(request,'dashboard/api_login_failed.html')


def license_detail(request):
        response = getDubPoints()
        json_response = response.json()['dub_points']
        index = len(json_response)
        totalDUBPoints = index
        totalActiveDUBPoints = 0
        totalSuspendedDUBPoints = 0
        totalTypeRecorderDUBPoints=0
        totalTypeAPIDUBPoints =0
        totalTypeMeetingDUBPoints =0
        totalAIDUBPoints = 0
        totalNonAIDUBPoints =0
        for i in range(0,index):
            #Check for Type
            if(json_response[i]["type"] == "Recorder"):
                totalTypeRecorderDUBPoints = totalTypeRecorderDUBPoints + 1
            elif(json_response[i]["type"] == "Api"):
                totalTypeAPIDUBPoints = totalTypeAPIDUBPoints + 1
            elif(json_response[i]["type"] == "Meeting"):
                totalTypeMeetingDUBPoints = totalTypeMeetingDUBPoints + 1
            #Check for Status
            if(json_response[i]["status"] == "Active"):
                totalActiveDUBPoints = totalActiveDUBPoints + 1
            else:
                totalSuspendedDUBPoints = totalSuspendedDUBPoints + 1
            #Check fo AI
            if(json_response[i]["ai"] == True):
                totalAIDUBPoints = totalAIDUBPoints + 1
            else:
                totalNonAIDUBPoints = totalNonAIDUBPoints + 1

        DUB_TotalDUBPoints = totalDUBPoints
        DUB_ActiveDUBPoints = totalActiveDUBPoints
        DUB_SuspendedDUBPoints = totalSuspendedDUBPoints
        DUB_RecorderDUBPoints = totalTypeRecorderDUBPoints
        DUB_APIDUBPoints = totalTypeAPIDUBPoints
        DUB_MeetingDUBPoints = totalTypeMeetingDUBPoints
        DUB_AIDUBPoints = totalAIDUBPoints
        DUB_NonAIDUBPoints = totalNonAIDUBPoints
       
        return render(request,'dashboard/license_detail.html',{'page_name':'License','DUB_TotalDUBPoints':DUB_TotalDUBPoints,'DUB_ActiveDUBPoints':DUB_ActiveDUBPoints,'DUB_SuspendedDUBPoints':DUB_SuspendedDUBPoints,'DUB_RecorderDUBPoints':DUB_RecorderDUBPoints,'DUB_APIDUBPoints':DUB_APIDUBPoints,'DUB_MeetingDUBPoints':DUB_MeetingDUBPoints,'DUB_AIDUBPoints':DUB_AIDUBPoints,'DUB_NonAIDUBPoints':DUB_NonAIDUBPoints,'page_name':'License Information Dashboard'})

def admin_user(request):
    response = getAdminUsers()
    admin_user_json = response.json()['users']
    page = request.GET.get('page', 1)
    paginator = Paginator(admin_user_json, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'dashboard/admin_user.html',{'users':users,'page_name':'Administrator User Information'})

def standard_user(request):
    response = getStandardUsers()
    standard_user_json = response.json()['users']
    page = request.GET.get('page', 1)
    paginator = Paginator(standard_user_json, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'dashboard/admin_user.html',{'users':users,'page_name':'Standard User Information'})

def data_export_csv(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')+" 11:22:03"
        to_date = request.POST.get('to_date')+" 11:22:03"
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        fdt_year = from_date.year
        fdt_month = from_date.month
        fdt_day = from_date.day


        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
        tdt_year = to_date.year
        tdt_month = to_date.month
        tdt_day = to_date.day
        f_date = date(fdt_year,fdt_month,fdt_day)
        t_date = date(tdt_year,tdt_month,tdt_day)
        day_duration = t_date - f_date
        if(day_duration.days > 30):
            error_msg ='Please enter a vaue between 1 and 30 days'
       
            return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export','error_msg':error_msg})
        else:
            #"from_date": "2020-06-09T00:00:00+01:00",
	        #"to_date": "2020-07-09T10:30:00+01:00"
    
            fn_from_date = f_date.isoformat()+'T00:00:00+01:00'
            fn_to_date = t_date.isoformat()+'T10:30:00+01:00'
            response = get_csv_dwnld_link(fn_from_date,fn_to_date)
            json_response = response.json()
            report_status = json_response['status']
            report_id = json_response['id']
            if(report_status == 'Active'):
                export_url = json_response['export_url']
                return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export','export_url':export_url})
            else:
                return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export','report_status':report_status})
            
            return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export'})

           
    else:
        return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export'})