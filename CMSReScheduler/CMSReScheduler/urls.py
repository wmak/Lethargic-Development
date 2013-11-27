from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CMSReScheduler.views.index', name='index'),
    #url(r'^registration/(?P<user_role>.*)/$', 'CMSReScheduler.views.registration', name='registration'),
    url(r'^rooms/(?P<room_code>.*)/$', 'CMSReScheduler.views.room_schedule', ),
    url(r'^schedule/(?P<department_name>.*)/(?P<instructor_name>.*)/$', 'CMSReScheduler.views.department_schedule'),
    url(r'^register/$', 'CMSReScheduler.views.register', name='register'),
    url(r'^admin/$', 'CMSReScheduler.views.admin', name='admin'),
    url(r'^admin/upload/$', 'CMSReScheduler.views.admin_upload', name='admin_upload'),
    url(r'^admin/users/$', 'CMSReScheduler.views.list_users', name='list_users'),
    url(r'^admin/users/(?P<username>.*)/profile/$', 'CMSReScheduler.views.admin_edit_profile', name='admin_edit_profile'),
    url(r'^admin/users/(?P<username>.*)/edit/$', 'CMSReScheduler.views.admin_edit_user', name='admin_edit_user'),
    url(r'^admin/users/(?P<username>.*)/delete/$', 'CMSReScheduler.views.delete_user', name='delete_user'),
    url(r'^room/room_capacities/$', 'CMSReScheduler.views.room_capacities'),
    url(r'^login/$', 'CMSReScheduler.views.login_view', name='login'),
    url(r'^logout/$', 'CMSReScheduler.views.logout_view', name='logout'),
    url(r'^profile/$', 'CMSReScheduler.views.edit_profile', name='edit_profile'),
    url(r'^my_user/$', 'CMSReScheduler.views.edit_user', name='edit_user'),
    url(r'^change_password/$', 'CMSReScheduler.views.change_password'),
    #this regex is not complete yet
    #it should only receive urls like: rooms/filter/capacity-building/50-IC/
    url(r'^(?P<model>.*)/filter/$', 'CMSReScheduler.views.filter', name = 'filter'),
    # url(r'^CMSReScheduler/', include('CMSReScheduler.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),

	url(r'^course/(?P<course>\w+)/(?P<section>.*)$', 'CMSReScheduler.views.course', name='course'),
    url(r'^user/(?P<user_id>\w+)$', 'CMSReScheduler.views.user', name='user'),
    url(r'^export/(?P<model>\w+)$', 'CMSReScheduler.views.export', name='export'),
)
