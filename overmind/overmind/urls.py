from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'overmind.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^hardware/', include('hardware.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
