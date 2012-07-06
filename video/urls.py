from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('video.views',
    url(r'^$', 'index', name='homepage'),
    url(r'^list$', 'video_list'),
    url(r'^import/$', 'importvideo', name="import_video"),
    url(r'^refresh/(?P<video_id>[\d]+)/$', 'refresh', name="refresh"),
    url(r'^convert/(?P<video_id>[\d]+)$', 'convert', name="convert"),
    url(r'play/(?P<filename>[\w\d\-]+)$', 'play', name="play"),
    url(r'delete/(?P<video_id>[\d]+)/$', 'delete', name='delete'),
    url(r'livecast/', 'livecast', name='livecast'),
)
