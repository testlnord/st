from django.conf.urls import patterns, include, url


from sur_tournament.views import main


urlpatterns = patterns('',
    url(r'^$', main),
)
