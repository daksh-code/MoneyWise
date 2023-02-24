from asyncio import tasks
from email import message
from unicodedata import category
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from requests import request
from django.contrib.auth.models import User
from urllib3 import HTTPResponse
from mainapp.models import StockDetail,UserPortfolio
from yahoo_fin.stock_info import *
import time
import queue
import pandas as pd 
import json
import numpy
from threading import Thread
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from send_mail_app.tasks import send_mail_func,send_mail_func_portfolio
from django_celery_beat.models import PeriodicTask, CrontabSchedule,IntervalSchedule
from datetime import date, datetime

# Create your views here.
@login_required(login_url='/authentication/login')
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

"""@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True"""

@login_required(login_url='/authentication/login')
def stockTracker(request):
    """is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")"""
    stockpicker = request.GET.getlist('stockpicker')
    stockshare=str(stockpicker)[1:-1]
    
    print(stockpicker,"MELLO HJIHI")
    data = {}
    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    # for i in stockpicker:
    #     result = get_quote_table(i)
    #     data.update({i: result})

    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
    end = time.time()
    time_taken =  end - start
    print(time_taken)
    print(data)
    return render(request, 'mainapp/stocktracker.html', {'data': data,'room_name':'track','selectedstock':stockshare})

@login_required(login_url='/authentication/login')
def stockDetail(request):

    if request.method=='GET':
        detailstock=request.GET['stockpicker']
        n_threads = 2
        thread_list = []
        que = queue.Queue()
        t1 = Thread(target=lambda q,arg1:q.put(get_quote_table(arg1)), args=(que,detailstock))
        t2 = Thread(target=lambda q,arg1:q.put(get_balance_sheet(arg1)), args=(que,detailstock))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        balance_sheet = que.get()
        temp_price_quote = que.get()
        temp_price_quote=temp_price_quote["Quote Price"]
        
        print(balance_sheet.columns)
        #balance_sheet.columns = ['Parameter', '2022-03-31', '2021-03-31', '2020-03-31','2019-03-31']
        print(balance_sheet)
        json_records = balance_sheet.reset_index().to_json(orient ='records')
        data=[]
        data = json.loads(json_records)
        print(data)
        context = {
            'd': data,
            'room_name':'track',
            "detailstock":detailstock,
            "temp_price_quote":temp_price_quote
        }
        return render(request, 'mainapp/stockdetail.html',context)
    if request.method=='POST':
        stockname=request.POST['stockname']
        quantity=request.POST['quantity']
        lockindate=request.POST['lockindate']
        price=request.POST['price']
        
        print(lockindate)
        UserPortfolio.objects.create(price=price,quantity=quantity,lockindate=lockindate,owner=request.user,
                               stockname=stockname)
       
        messages.success(request, 'Order Placed successfully')
        return redirect('stockportfolio')

@login_required(login_url='/authentication/login')
def stockPortfolios(request):
    portfolios=UserPortfolio.objects.filter(owner=request.user)
    finalrep={}
    def get_category_amount(portfolio):
        amount=0
        filtered_by_category=portfolios.filter(stockname=portfolio)
        for item in filtered_by_category:
            amount+=(item.price*item.quantity)
        return amount
    def get_category(portfolio):
        return portfolio.stockname

    category_list=list(set(map(get_category,portfolios)))
    for x in portfolios:
        for y in category_list:
            finalrep[y]=get_category_amount(y)
    print(finalrep)
    return JsonResponse({"stock_user_data":finalrep},safe=False)

def portfolio_view(request):
    portfolio=UserPortfolio.objects.filter(owner=request.user)
    print(date.today())
    datetoday=date.today()
    return render(request,'mainapp/stats.html',{"portfolio":portfolio,"datetoday":datetoday})

def delete_stock(request,id):
    deleteme=UserPortfolio.objects.get(pk=id)
    deleteme.delete()
    return redirect('stockportfolio')

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

@login_required(login_url='/authentication/login')
def schedule_mail(request):
    schedule1, created = CrontabSchedule.objects.get_or_create(hour = 9, minute = 15)
    schedule2, created = CrontabSchedule.objects.get_or_create(hour = 15, minute = 30)
    task1 ,created= PeriodicTask.objects.get_or_create(crontab=schedule1, name="schedule_mail_task_at "+"9:15", task='send_mail_app.tasks.send_mail_func') #, args = json.dumps([list(lockinends)],default=str))
    task2 ,created= PeriodicTask.objects.get_or_create(crontab=schedule2, name="schedule_mail_task_at "+"3:30", task='send_mail_app.tasks.send_mail_func_portfolio')

    return HttpResponse("Done")


    
    
    