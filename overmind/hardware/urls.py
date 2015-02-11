from django.conf.urls import patterns, url

from hardware import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)