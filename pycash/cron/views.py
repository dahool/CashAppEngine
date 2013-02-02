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
from django.core import serializers
from pycash.decorators import json_response
from pycash.models import SyncRecord
from pycash.services.DropboxService import StorageService
from pycash.services import DateService, StatsService
import datetime
import StringIO
import gzip
from pycash.services import RequestUtils
from pycash.services.Utils import logger
from django.core.mail import mail_managers as send_mail

@json_response
def backup(request):
    if RequestUtils.param_exist("date", request.REQUEST):
        today = datetime.datetime.strptime(request.REQUEST['date'],"%Y%m%d")
    else:
        today = datetime.date.today()
    fromDate = DateService.midNight(today - datetime.timedelta(days=7))
    toDate = DateService.midNight(today)
    try:
        records = SyncRecord.objects.filter(created__gte=fromDate, created__lt=toDate)
        data = serializers.serialize("xml", records);
        filename = "%s_cashbackup.xml" % today.strftime("%Y%m%d")
        filedata = StringIO.StringIO()
        zipped = gzip.GzipFile(filename, 'wb', fileobj=filedata)
        zipped.write(data)
        zipped.close()
        st = StorageService()
        st.file_put(filedata.getvalue(), filename + ".gz")
        error = ''
    except Exception, e:
        logger.error(str(e))
        send_mail("EXPORT ERROR", 'Processing %s.\n\nError: %s' % (today.strftime("%Y-%m-%d"), str(e)))
        error=str(e)
    return {'processed': today.strftime("%Y-%m-%d"), 'sync': records.count(), 'error': error}

@json_response
def updateevent(request):
    from pycash.management.commands.updateevent import Command
    response = StringIO.StringIO()
    cmd = Command()
    cmd.stdout = response
    cmd.handle()
    return {'process': response.getvalue()}
    
@json_response
def generatestats(request):
    StatsService.generate()
    return {'process': 'ok'}
    
@json_response
def generatemonthstats(request):
    StatsService.generate_current()
    return {'process': 'ok'}    
    