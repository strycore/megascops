from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^accounts/login/error/$', direct_to_template,
        {'template': 'registration/login_error.html'}, name='login_error'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('video.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
