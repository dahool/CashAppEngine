from django.conf.urls.defaults import *
from pycash.cash.controllers import CategoryController as controller

urlpatterns = patterns('',
    (r'^list$', controller.list),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
    (r'^$', controller.index)
)
