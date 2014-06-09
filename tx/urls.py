from django.conf.urls import patterns, include, url
from main import views
from main.api import ItemResource

item_resource = ItemResource()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^toolbox/', views.toolbox, name='toolbox'),
    url(r'^api/', include(item_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
