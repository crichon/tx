from django.conf.urls import patterns, include, url
from main import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^toolbox/', views.xls, name='toolbox'),
    url(r'^admin/', include(admin.site.urls)),
)
