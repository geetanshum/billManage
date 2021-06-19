from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.utils import formats
from billmanage.models import *
from datetime import datetime
from awgp.common.json import JSON
from awgp.common.response import Response
from awgp.django.database import DB
from awgp.common.data import Recordset
from django.core import serializers
from django.http import JsonResponse
import json
from django.db.models import Q
from django.contrib import messages


def subscription(request):
    template = loader.get_template('webforntjoinform/index.html')
    sForm = billformDetail()
    context = {"joinform":sForm}
    return HttpResponse(template.render(context, request))

def addjoinsubscription(request):
    s = bill()
    s.billno = request.POST["billno"]
    s.item = request.POST["item"]
    s.date = request.POST["date"]
    s.amount = request.POST["amount"]
    s.remark = request.POST["remark"]
    s.user = request.user
    s.save()
    template = loader.get_template('webforntjoinform/alert.html')
    context = {}
    return HttpResponse(template.render(context, request))

def reportbill(request):
    resp = Response()
    r = Recordset()
    contaxt = {}
    var1 = '%'
    if request.method == "POST":
        fromdt = str(request.POST.get("from_date"))
        todt = str(request.POST.get("to_date"))
        remark = str(request.POST.get("remark"))
        status = str(request.POST.get("status"))
        fromdate = datetime.strptime(fromdt, '%Y-%m-%d')
        todate = datetime.strptime(todt, '%Y-%m-%d')
        # print(status)
        if status == "" and remark == "":
            # print(fromdate)
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate).order_by("date")

        elif str(request.POST.get("remark")) == "" and status != "":
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate, status=status).order_by("date")

        elif remark != "" and status == "":
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate,remark__startswith = remark).order_by("date")
            # print("hello")
            
        else:
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate,remark__startswith = remark, status=status).order_by("date")

        r.fromQueryset(itbill,{"code":"id","bill":"billno","date":{"name":"date","format":"%d-%m-%Y"},"remark":"remark","amount":"amount", "status":"status"})
        resp.success("data ok")
        resp.setExtra(r.data)
        # print(itbill)
        return HttpResponse(resp.getJson())
    return render(request,"webforntjoinform/report.html",context=contaxt)

def print_view(request):
    resp = Response()
    r = Recordset()
    contaxt = {}
    if request.method == "POST":
        fromdt = str(request.POST.get("from_date"))
        todt = str(request.POST.get("to_date"))
        remark = str(request.POST.get("remark"))
        status = str(request.POST.get("status"))
        fromdate = datetime.strptime(fromdt, '%Y-%m-%d')
        todate = datetime.strptime(todt, '%Y-%m-%d')
        # changed by deepak $ chauhan
        
        if status == "" and remark == "":
            # print(fromdate)
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate).order_by("date")

        elif str(request.POST.get("remark")) == "" and status != "":
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate, status=status).order_by("date")

        elif remark != "" and status == "":
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate,remark__startswith = remark).order_by("date")
            # print("hello")       
        else:
            itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate,remark__startswith = remark, status=status).order_by("date")

        # end changes

        # # print(remark)
        # if str(request.POST.get("remark")) == "":
        #     # print(fromdate)
        #     itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate).order_by("date")
        # else:  
        #     itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate,remark__startswith = remark).order_by("date")
        r.fromQueryset(itbill,{"date":{"name":"date","format":"%d-%m-%Y"},"remark":"remark","amount":"amount", "status":"status"})
        resp.success("data ok")
        resp.setExtra(r.data)
        # print(itbill)
        return HttpResponse(resp.getJson())      
    return render(request, "webforntjoinform/print.html",context=contaxt)

def statusUpdate(request):
    dt = request.POST.get("data")
    id = JSON.fromString(dt)
    # print(id)
    # resp = Response()
    # r = Recordset()
    data = bill.objects.filter(id=id)
    obj = get_object_or_404(bill ,id=id)
    if obj.status == 'U':
        data = bill.objects.filter(id=id).update(status='P')
        print("Marked as Paid")
        messages.info(request,"Marked as Paid")
        return HttpResponse("Marked as Paid")
    # elif obj.status == 'P':
    #     data = bill.objects.filter(id=id).update(status='U')
    #     print("Marked as UnPaid")
    #     return HttpResponse("Marked as UnPaid")
    else:
        messages.info(request,"Bill is already paid")
        return HttpResponse("Bill is already paid")
    print(data)
    # r.fromQueryset(data,{"amount":"amount"})
    # resp.success("status changed")
    # resp.setExtra(r.data)