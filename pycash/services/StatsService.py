# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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
from pycash.services import DateService
from pycash.models import Expense, Income, StatsData, CategoryStatsData
from django.conf import settings
from pycash.services.Utils import logger

def generate_current():
    date = DateService.todayDate() 
    fromDate = DateService.firstDateOfMonth(date)
    toDate = DateService.lastDateOfMonth(date)
    create_stats(fromDate, toDate)
    
def generate():
    date = DateService.addMonth(DateService.todayDate(),-1) 
    fromDate = DateService.addMonth(DateService.firstDateOfMonth(date),-6)
    toDate = DateService.lastDateOfMonth(date)
    
    values = DateService.getMonthRange(fromDate, toDate)

    for value in values:
        create_stats(*value)
    
def create_category_stats(fromDate, toDate):
    logger.debug("Process Categories %s - %s" % (fromDate, toDate))
    month = fromDate.strftime('%Y%m')
    
    CategoryStatsData.objects.filter(month=month).delete()

    q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)
    co = 0
    for expense in q:
        co += 1
        csd, c = CategoryStatsData.objects.get_or_create(month=month, category=expense.subCategory.category)
        csd.amount = csd.amount + expense.amount
        csd.save()
    
    logger.debug("Processed %s" % co)
    
def create_stats(fromDate, toDate):
    logger.debug("Process %s - %s" % (fromDate, toDate))
    month = fromDate.strftime('%Y%m')
    
    incomeSum = 0
    for income in Income.objects.filter(period__gte=fromDate, period__lte=toDate):
        incomeSum += income.amount
    
    try:
        data = StatsData.objects.get(pk=month)
    except StatsData.DoesNotExist:
        data = StatsData(month=month)
        
    data.incomes = incomeSum
    
    expenseSum = 0
    
    q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)

    defaultpt = getattr(settings,'STATS_PAYMENT_TYPE', None)
    if defaultpt:
        q = q.filter(paymentType__id=defaultpt)
                
    for expense in q:
        expenseSum += expense.amount
    
    data.expenses= expenseSum
    
    data.save()
    
    create_category_stats(fromDate, toDate)
    
def create_chart():
    import pygal
    #chart = pygal.Line()
    chart = pygal.Bar()
    chart.title = 'Gastos'
    
    q = StatsData.objects.all().order_by('-month')[:6]
    data = sorted(q, key=lambda d: d.month)
    
    labels = []
    expenses = []
    incomes = []
    for d in data:
        labels.append(d.display_month)
        expenses.append(float(d.expenses))
        incomes.append(float(d.incomes))
    
    chart.x_labels = labels   
    logger.debug(labels) 
    chart.add('Gastos', expenses)
    chart.add('Ingresos', incomes)
    
    return chart.render()
