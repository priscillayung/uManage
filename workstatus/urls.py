from django.conf.urls.defaults import patterns, include, url
from mail.views import*
from sendingMassEmail.views import*

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'workstatus.views.home', name='home'),
    # url(r'^workstatus/', include('workstatus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', read),
    (r'^updates/$',parser),
    (r'^updates/(\w+)/$', user_page),
)