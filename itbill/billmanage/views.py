from django.shortcuts import render
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
    if request.method == "POST":
        fromdt = str(request.POST.get("from_date"))
        todt = str(request.POST.get("to_date"))
        fromdate = datetime.strptime(fromdt, '%Y-%m-%d')
        todate = datetime.strptime(todt, '%Y-%m-%d')
        itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate).order_by("date")
        r.fromQueryset(itbill,{"code":"id","bill":"billno","date":{"name":"date","format":"%d-%m-%Y"},"remark":"remark","amount":"amount"})
        resp.success("data ok")
        resp.setExtra(r.data)
        # print(r.data)
        return HttpResponse(resp.getJson())
    return render(request,"webforntjoinform/report.html",context=contaxt)

def print_view(request):
    resp = Response()
    r = Recordset()
    contaxt = {}
    if request.method == "POST":
        fromdt = str(request.POST.get("from_date"))
        todt = str(request.POST.get("to_date"))
        fromdate = datetime.strptime(fromdt, '%Y-%m-%d')
        todate = datetime.strptime(todt, '%Y-%m-%d')
        itbill = bill.objects.filter(date__gte=fromdate,date__lte=todate).order_by("date")
        r.fromQueryset(itbill,{"date":{"name":"date","format":"%d-%m-%Y"},"amount":"amount"})
        resp.success("data ok")
        resp.setExtra(r.data)
        # print(r.data)
        return HttpResponse(resp.getJson())      
    return render(request, "webforntjoinform/print.html",context=contaxt)