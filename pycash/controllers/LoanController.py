# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
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

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pycash.models import Person, Loan, Payment
from pycash.services import JsonParser, DateService
from pycash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError, connection
try:
    import _mysql_exceptions
except:
    import pycash.exceptions as _mysql_exceptions
from pycash.decorators import json_response

from pycash.validators import validate_amount
from django.core.exceptions import ValidationError

from pycash.controllers.PaymentController import getPaymentRemain

@render('cash/loan/index.html')
def index(request):
    return {}

@json_response
def list(request):
    req = request.REQUEST
    q = Loan.objects.filter()
    if param_exist("person.id",req):
        q = q.filter(person=req['person.id'])    
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if not param_exist("all",req):
        q = q.filter(remain__gt=0)
    if param_exist("limit",req):
        start = int(req['start'])
        limit = int(req['limit'])
        list = q[start:start+limit]
    else:
        list = q
        
    res = []
    for exp in list:
        if exp.remain == 0:
            partial = 0
        else:
            partial = exp.amount / exp.instalments 
        if exp.remain < partial:
            partial = exp.remain
             
        res.append({'id': exp.id, 'amount': exp.amount, 'date': exp.date,
                    'reason': exp.reason, 'person': exp.person.name, 'instalments': exp.instalments,
                    'personId': exp.person.id, 'balance': exp.remain, 'partial': partial})
    
    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return data

def from_request(request):
    req = request.REQUEST
    p = Person(pk=req['person.id'])
    l = Loan(person=p,amount=req['amount'],date=DateService.parseDate(req['date']), reason=req['reason'], remain=req['amount'])
    if param_exist("id",req):
        l.pk = req['id']

    if param_exist("instalments",req):
        l.instalments = req['instalments']
    else:
        l.instalments = 1
    return l
        
def process_request(request):
    req = request.REQUEST
    p = Person(pk=req['person.id'])

    amount=req['amount']
    #validate amount
    validate_amount(amount)
    
    reason=req['reason']
    if not reason or reason.strip() == '':
        raise ValidationError(_('Reason is required.'), code='required')
        
    date=DateService.parseDate(req['date'])
    
    l = Loan(person=p, amount=amount, reason=reason, remain=amount, date=date)
    if param_exist("id",req):
        l.pk = req['id']
        l.remain = "%.2f" % getPaymentRemain(l)
        
    if param_exist("instalments",req):
        l.instalments = req['instalments']
    else:
        l.instalments = 1
    return l

@json_response
def save_or_update(request):
    data = '{"success":true}'
    try:
        l = process_request(request)
        l.save()
    except _mysql_exceptions.Warning:
        pass        
    except ValidationError, va1:
        data = '{"success":false, "msg": "%s: %s"}' % (va1.code, "".join(va1.messages))
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)    
    return data

@json_response
def delete(request):
    l = Loan(pk=request.REQUEST['id'])
    try:
        l.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)     
    return data
