from django.conf.urls.defaults import *
from pycash.cash.controllers import IncomeController as controller

urlpatterns = patterns('',
    (r'^stats$', controller.stats),                       
    (r'^list$', controller.list),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
    (r'^$', controller.index)
)

    

