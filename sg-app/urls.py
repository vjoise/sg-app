from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'query$', 'hello.sg-app.query'), #ending with url pattern should be used
    url(r'refresh$', 'hello.sg-app.refresh'), #ending with url pattern should be used
    url(r'route$', 'hello.sg-app.refreshRoute'),
)
