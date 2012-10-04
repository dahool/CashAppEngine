from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pycash.cron.views',
    url(r'^backup/$', 'backup'),
    url(r'^updateevent/$', 'updateevent'),
    url(r'^generatestats/$', 'generatestats'),
)