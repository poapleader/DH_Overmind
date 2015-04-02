from django.conf.urls import patterns, url

from hardware import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^(?P<kiosk_id>\d+)$', views.detail, name='detail'),
)