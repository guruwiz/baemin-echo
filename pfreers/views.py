import types
from django.core import paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import PfreeEateries
from django.utils import timezone 
from .forms import PfreeEateriesForm
from datetime import datetime
from django.core.paginator import Paginator

import json
from decouple import config
import pandas as pd
from pandas import DataFrame
from pprint import pprint as pp
from simple_salesforce import Salesforce, SalesforceLogin, SFType

def index(request):
    """
    Output for PfreeEateries
    """
    # page count
    page = request.GET.get('page', '1')

    # query
    qry = 'SELECT Id, eatery_types__C, eatery_name__C, echo_level__c, echof_cont_cnt__c, perf_rate__C, join_date__c FROM pfree_eatery__c ORDER BY join_date__c DESC'
    #PfreeEateries_list = PfreeEateries.objects.order_by('-create_date')
    
    qr = SOQL(qry)
    PfreeEateries_list = qr.values

    #print(PfreeEateries_list)

    # handling pages
    paginator = Paginator(PfreeEateries_list, 10) # Show 10 per page
    page_obj = paginator.get_page(page)
    #print(data)
    #context = {'PfreeEateries_list': PfreeEateries_list}
    context = {'PfreeEateries_list': page_obj}
    return render(request, 'pfreers/pfreeElist.html', context)

def detail(request, PfreeEateries_id):
    """
    List of PfreeEateries
    """
    elist = PfreeEateries.objects.get(id=PfreeEateries_id)
    context = {'elist': elist}
    return render(request, 'pfreers/pfreeElist_detail.html', context)

def PfreeEateries_create(request):
    """
    Register a eatery
    """
    '''
            PfreeEateries = form.save(commit=False)
            PfreeEateries.echolv = 'BLUE'
            PfreeEateries.perf = 0
            PfreeEateries.create_date = today.isoformat()+'Z'
            PfreeEateries.save()
    '''
    username = config('username')
    password = config('password')
    security_token = config('security_token')
    domain = 'login'

    #sf = Salesforce(username=username, password=password, security_token=security_token, domain=domain)
    session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
    #sf = Salesforce(instance_url='http://'+instance , session_id=session_id)
    sf = Salesforce(instance=instance , session_id=session_id)

    pfree_eatery__c = SFType('pfree_eatery__c', session_id, instance)
    ecount = 0
    prate = 0
    if request.method == 'POST':
        #form = PfreeEateriesForm(request.POST)
        etypes = request.POST['eatery_types']
        name = request.POST['eatery_name']
        today = timezone.now()
 
        data = {
            'eatery_types__c' : etypes,
            'eatery_name__c' : name,
            'echo_level__c' : 'BLUE',
            'echof_cont_cnt__c' : ecount,
            'perf_rate__c' : prate,
            'join_date__c' : today.isoformat() + 'Z'
        }
        response = pfree_eatery__c.create(data)
        print(response)
        return redirect('/pfreers/')
    else:
        form = PfreeEateriesForm()
        context = {'form': form}
        return render(request, 'pfreers/PfreeEateries_form.html', context)

def SOQL(SOQL):
    username = config('username')
    password = config('password')
    security_token = config('security_token')
    domain = 'login'

    #sf = Salesforce(username=username, password=password, security_token=security_token, domain=domain)
    session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
    #sf = Salesforce(instance_url='http://'+instance , session_id=session_id)
    sf = Salesforce(instance=instance , session_id=session_id)
    
    qryResult = sf.query(SOQL)
    print('Record count {0}'.format(qryResult['totalSize']))
    isDone = qryResult['done']
    
    if isDone == True:
        df = DataFrame(qryResult['records'])
    while isDone != True:
        try:
            if qryResult['done'] != True:
                df = df.append(DataFrame(qryResult['records']))
                qryResult = sf.query_more(qryResult['nextRecorsdUrl'], True)
            else:
                df = df.append(DataFrame(qryResult['records']))
                isDone = True
                print('Completed')
                break
            
        except NameError:
            df = DataFrame(qryResult['records'])
            qry = sf.query_more(qryResult['nextRecordsUrl'], True)        
    
    df = df.drop('attributes', axis = 1)
    return df;