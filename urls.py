from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'megascops.video.views.index'),
    url(r'^list$', 'megascops.video.views.video_list'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^import/$', 'megascops.video.views.importvideo', name="import_video"),
    url(r'^convert/(?P<video_id>[\d]+)$', 'megascops.video.views.convert',
        name="convert"),
    url(r'play/(?P<filename>[\w\d\-]+)$', 'megascops.video.views.play',
        name="play"),
    url(r'livecast/', 'megascops.video.views.livecast'),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
