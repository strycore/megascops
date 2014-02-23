# pylint: disable=C0103
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'video.views',
    url(r'^$', 'index', name='homepage'),
    url(r'^user/(?P<username>[\w_-]+)/$', 'user_profile_show',
        name="user_profile_show"),
    url(r'^list/$', 'video_list',
        name="video_list"),
    url(r'^analyze/$', 'analyze_url', name="analyze_url"),
    url(r'^import/$', 'launch_import', name='launch_import'),
    url(r'^refresh/(?P<video_id>[\d]+)/$', 'refresh', name="refresh"),
    url(r'^convert/(?P<video_id>[\d]+)$', 'convert', name="convert"),
    url(r'^play/(?P<filename>[\w\d\-]+)/(?P<pk>[\d]+)/$', 'play',
        name="play"),
    url(r'^delete/(?P<video_id>[\d]+)/$', 'delete', name='delete'),
    url(r'^livecast/$', 'livecast', name='livecast'),
    url(r'^webrtc/$', 'webrtc', name='webrtc'),
)
