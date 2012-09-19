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
from pycash.models import PaymentType, SubCategory, Expense, Person, Loan, Tax
import datetime
from django.db.models import Sum

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
    q = Expense.objects.filter(date__lte = datetime.datetime.now()).exclude(date__lt = datetime.datetime.now() - datetime.timedelta(days=5))
    q = q.order_by("-date")
    return {"settings": settings,
            "list": q,
            "today": datetime.date.today()}

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
def loans_payments_add(request, id):
    l = Loan.objects.get(pk=id)
    return {"loan": l}

@render('mobile/loans_add.html')
def loans_add(request, id):
    p = Person.objects.get(pk=id)
    return {"person": p}
   
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