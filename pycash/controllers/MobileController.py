# -*- coding: utf-8 -*-
"""Copyright (c) 2011-2012 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from common.view.decorators import render

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from pycash.models import PaymentType, SubCategory, Expense, Person, Loan, Tax, Payment, Income
import datetime
from django.db.models import Sum
from pycash.services import DateService, RequestUtils

@render('mobile/expenses_frm.html')
def expensesAdd(request, id = None):
    if id:
        e = Expense.objects.get(pk=id)
    else:
        e = None

    pType = PaymentType.objects.all().order_by("name")
    #cList = SubCategory.objects.all().order_by("category__name", "name")
    cList = SubCategory.objects.all().order_by("name")
    
    return {"paymentTypeList": pType,
            "categoryList": sorted(cList, key=lambda scat: scat.category.name),
            "expense": e}

@render('mobile/expenses_list.html')
def expensesList(request):
    req = request.POST
    if RequestUtils.param_exist("toDate", req):
        toDate = DateService.parseDate(req['toDate'])
    else:
        toDate = datetime.datetime.now()
    if RequestUtils.param_exist("fromDate", req):
        fromDate = DateService.parseDate(req['fromDate'])
    else:
        fromDate = toDate - datetime.timedelta(days=5)  
    q = Expense.objects.filter(date__gte = DateService.midNight(fromDate), date__lte = DateService.midNight(toDate, True))
    q = q.order_by("-date")
    return {"settings": settings,
            "list": q,
            "today": datetime.date.today(),
            "filterStart": fromDate,
            "filterEnd": toDate}

@render('mobile/loans.html')
def loansHome(request):
    q = Person.objects.all()
    q = q.order_by("name")
    return {"list": q}

@render('mobile/loans_list.html')
def loans_list(request, id):
    p = Person.objects.get(pk=id)
    #llist = p.loans.active().order_by("date")
    llist = p.loans.active()
    if (llist.count() > 0):
        #total = p.loans.active().aggregate(total=Sum('remain'))['total']
        # appengine do not support functions
        total = 0
        for loan in llist:
            total += loan.remain
    else:
        total = 0
    return {"person": p,
            "list": sorted(llist, key=lambda loan: loan.date),"total": total}

@render('mobile/loans_payments.html')
def loans_payments(request, id):
    l = Loan.objects.get(pk=id)
    return {"loan": l, "total": l.amount - l.remain}

@render('mobile/loans_payments_add.html')
def loans_payments_add(request, id, pId = None):
    l = Loan.objects.get(pk=id)
    amount = None
    if pId:
        p = Payment.objects.get(pk=pId)
    else:
        p = None
        amount = l.amount / l.instalments
        if amount > l.remain:
            amount = l.remain
    return {"loan": l, "payment": p, "remain": amount}

@render('mobile/loans_add.html')
def loans_add(request, id, loanId = None):
    p = Person.objects.get(pk=id)
    if loanId:
        l = Loan.objects.get(pk=loanId)
    else:
        l = None
    return {"person": p, "loan": l}
   
@render('mobile/tax.html') 
def taxHome(request):
    limit = (datetime.datetime.now() + datetime.timedelta(days=5))
    upcoming = Tax.objects.filter(expire__lte=limit).order_by('expire')
    return {"list": upcoming}

@render('mobile/tax_list.html') 
def taxList(request):
    tlist = Tax.objects.all().order_by('service')
    return {"list": tlist}

@render('mobile/tax_add.html')
def taxAdd(request, id = None):
    if id:
        e = Tax.objects.get(pk=id)
    else:
        e = None

    pType = PaymentType.objects.all().order_by("name")
    #cList = SubCategory.objects.all().order_by("category__name", "name")
    cList = SubCategory.objects.all().order_by("name")
    
    return {"paymentTypeList": pType,
            "categoryList": sorted(cList, key=lambda scat: scat.category.name),
            "tax": e}
    
@render('mobile/tax_pay.html')
def taxPay(request, id):
    e = Tax.objects.get(pk=id)
    return {"tax": e}    

@render('mobile/income_list.html') 
def incomeList(request):
    req = request.POST
    if RequestUtils.param_exist("fromDate", req):
        fromDate = DateService.parseDate(req['fromDate'])
    else:
        dt = datetime.date.today() - datetime.timedelta(days=30*5)
        fromDate = datetime.date(dt.year, dt.month, 1)
    q = Income.objects.filter(period__gte = DateService.midNight(fromDate))
    q = q.order_by("-period")
    return {"list": q,
            "filterStart": fromDate}

@render('mobile/income_add.html')
def incomeEdit(request, id):
    e = Income.objects.get(pk=id)
    return {"income": e}    
