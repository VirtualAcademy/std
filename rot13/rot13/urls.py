from django.conf.urls import patterns, include, url
from django.contrib import admin
from rot13app import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rot13.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	(r'^rot13/$',views.cyph, {'tempname': 'rot13.html'}),
)
