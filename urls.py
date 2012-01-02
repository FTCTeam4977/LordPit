from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^LordScout/$', 'LordScout.views.index'),
	url(r'^LordScout/(?P<team_id>\d+)/info$', 'LordScout.views.teamview'),
	url(r'^LordScout/import$', 'LordScout.views.importScouting'),
	
    # Examples:
    # url(r'^$', 'LordPit.views.home', name='home'),
    # url(r'^LordPit/', include('LordPit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
