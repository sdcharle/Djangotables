from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import djangoweb
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djangoweb/', include('djangoweb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^cds/$', 'djangoweb.sdc.views.cds'),
    (r'^editor/$', 'djangoweb.sdc.views.editor'),
    (r'^delete/$', 'djangoweb.sdc.views.deleteCD'),
    (r'^update/$', 'djangoweb.sdc.views.updateCD'),
    (r'^add/$', 'djangoweb.sdc.views.addCD'),
)

# to serve static stuff via Django, not a strategy for success
# see this handy page: http://arthurkoziel.com/2008/09/02/handling-static-files-django/
if djangoweb.settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static_media/(?P<path>.*)$', 
        'serve', {
        'document_root': '/Users/scharlesworth/Djangotables/djangoweb/static_media',
        'show_indexes': True }),)
