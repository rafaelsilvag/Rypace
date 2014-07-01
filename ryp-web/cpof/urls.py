from django.conf.urls import patterns, include, url
import xadmin
xadmin.autodiscover()
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cpof.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(xadmin.site.urls)),
)
