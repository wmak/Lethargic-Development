from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CMSReScheduler.views.index', name='index'),
    url(r'^schedule/(?P<instructor>.*)/$', 'CMSReScheduler.views.instructor_schedule' ),
    url(r'^registration/(?P<user_role>.*)/$', 'CMSReScheduler.views.registration', name='registration'),
    url(r'^admin/$', 'CMSReScheduler.views.admin', name='admin'),
    url(r'^admin/upload/$', 'CMSReScheduler.views.admin_upload', name='admin_upload'),
    url(r'^rooms/(?P<room_code>.*)/$', 'CMSReScheduler.views.room_schedule', ),
    #this regex is not complete yet
    #it should only receive urls like: rooms/filter/capacity-building/50-IC/
    url(r'^(?P<model>.*)/filter/(?P<fields>.*)/(?P<values>.*)/$', 'CMSReScheduler.views.filter', name = 'filter'),
    # url(r'^CMSReScheduler/', include('CMSReScheduler.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),

	url(r'^course/(?P<course>\w+)/(?P<section>.*)$', 'CMSReScheduler.views.course', name='course'),
)
