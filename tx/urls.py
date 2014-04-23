from django.conf.urls import patterns, include, url
from main import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^toolbox/', views.toolbox, name='toolbox'),
    url(r'^admin/', include(admin.site.urls)),
)
