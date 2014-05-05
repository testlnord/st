from django.conf.urls import patterns, include, url


from sur_tournament.views import *


urlpatterns = patterns('',
    url(r'^$', main),
    url('add_tour', add_tour),
    url('tour/(?P<id>\d*)/$', tour),
    url('users/(.*)/$', users),
    url('contact/$', contact),
)
