from django.conf.urls.defaults import patterns, url
from views import nagios_landings


urlpatterns = patterns('',
    url(r'^nagios$', nagios_landings, name='nagios_landings'),
)
