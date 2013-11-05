from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CMSReScheduler.views.home', name='home'),
    url(r'^schedule/(?P<instructor>.*)/$', 'CMSReScheduler.views.instructor_schedule' ),
    url(r'^registration/(?P<user_role>.*)/$', 'CMSReScheduler.views.registration', name='registration'),
    url(r'^csvimport/(?P<model_type>.*)/$', 'CMSReScheduler.views.csvimport', name='csvimport'),
    url(r'^admin/$', 'CMSReScheduler.views.admin', name='admin'),
    url(r'^admin/upload/$', 'CMSReScheduler.views.admin_upload', name='admin_upload'),
    # url(r'^CMSReScheduler/', include('CMSReScheduler.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),

	url(r'^course/(?P<course>\w+)/$', 'CMSReScheduler.views.course', name='course'),
)
