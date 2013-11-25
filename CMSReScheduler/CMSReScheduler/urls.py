from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CMSReScheduler.views.index', name='index'),
    url(r'^schedule/(?P<instructor>.*)/$', 'CMSReScheduler.views.instructor_schedule' ),
    url(r'^register/$', 'CMSReScheduler.views.register', name='register'),
    url(r'^admin/$', 'CMSReScheduler.views.admin', name='admin'),
    url(r'^admin/upload/$', 'CMSReScheduler.views.admin_upload', name='admin_upload'),
    url(r'^admin/users/all$', 'CMSReScheduler.views.list_users', name='list_users'),
    url(r'^admin/users/(?P<username>.*)/profile/$', 'CMSReScheduler.views.admin_edit_profile', name='admin_edit_profile'),
    url(r'^login/$', 'CMSReScheduler.views.login_view', name='login'),
    url(r'^logout/$', 'CMSReScheduler.views.logout_view', name='logout'),
    url(r'^profile/$', 'CMSReScheduler.views.edit_profile', name='edit_profile'),
    url(r'^user/edit/$', 'CMSReScheduler.views.edit_user', name='edit_user'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change'),
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
