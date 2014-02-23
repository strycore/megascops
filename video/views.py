"""Megascops core views"""
#pylint: disable=E1101
import time

from django.http import Http404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import (render_to_response, get_object_or_404,
                              redirect, render)

from .models import Video
from .quvi import Quvi
from .tasks import fetch_video, encode_task


def index(request):
    """Homepage"""
    videos = Video.objects.ready().filter(private=False)
    return render(request, 'index.html', {'videos': videos})


def video_list(request):
    """List of all videos"""
    videos = Video.objects.ready().filter(private=False)
    return render(request, 'video_list.html', {
        'videos': videos
    })


@login_required
def analyze_url(request):
    """ Gathers information with quvi about videos on a given URL. """
    url = request.GET.get("url")
    quvi = Quvi(url)
    request.session['current_quvi'] = quvi.json
    return render(request, 'video/analyze.html', {'quvi': quvi})


@login_required
def launch_import(request):
    dump = request.session['current_quvi']
    quvi = Quvi(dump=dump)
    # Check if the video has already been downloaded
    video = Video()
    video.user = request.user
    video.title = quvi.title
    video.extension = quvi.stream.extension
    video.page_url = quvi.url
    video.filename = slugify(quvi.title)
    video.duration = quvi.duration
    video.state = "DOWNLOAD_INIT"
    video.host = quvi.host
    video.save()
    fetch_video.delay(quvi.json, video.id)
    return render(request, 'import.html', {'video': video})


@login_required
def refresh(request, video_id):
    """Update the status of a video being imported"""
    video = get_object_or_404(Video, pk=video_id)
    return render_to_response('video/import.html', {'video': video},
                              context_instance=RequestContext(request))


@login_required
def convert(request, video_id):
    """Convert a video to html5 format"""
    video = get_object_or_404(Video, pk=video_id)
    if video.user != request.user:
        raise Http404
    video.state = "CONVERTING"
    video.save()
    encode_task.delay(video.id)
    return redirect("/")


def play(request, filename, pk):
    """Show a video player for the selected video"""
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'video/play.html', {
        'video': video
    })


@login_required
def delete(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    return render(request, 'deleted.html')


def livecast(request):
    """Experimental livecast"""
    timestamp = int(time.time())
    return render(request, 'livecast.html', {
        'host': 'newport.strycore.com',
        'webcam_port': '8090',
        'screencast_port': '8091',
        'timestamp': timestamp
    })


def webrtc(request):
    return render(request, "video/webrtc.html")
