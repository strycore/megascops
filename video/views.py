"""Megascops core views"""
#pylint: disable=E1101
import time

from django.http import Http404
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Video
from .quvi import Quvi
from . import utils
from .tasks import fetch_video, encode_task


def index(request):
    """Homepage"""
    videos = Video.objects.ready().filter(private=False)
    return render(request, 'index.html', {'videos': videos})


def user_error(request):
    message = request.session.get('user_error')
    if not message:
        raise Http404
    return render(request, 'video/error.html', {'message': message})


def video_list(request):
    """List of all videos"""
    videos = Video.objects.ready().filter(private=False)
    return render(request, 'video_list.html', {
        'videos': videos
    })


@login_required
def analyze_url(request):
    """ Gathers information with quvi about videos on a given URL. """
    try:
        url = utils.sanitize_url(request.GET.get("url"))
    except ValueError as ex:
        request.session['user_error'] = ex.message
        return redirect(reverse('user_error'))
    try:
        quvi = Quvi(url)
    except ValueError:
        request.session['user_error'] = (
            "Impossible to get video information from %s" % url
        )
        return redirect(reverse('user_error'))
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
    return render(request, 'video/import.html', {'video': video})


@login_required
def refresh(request, video_id):
    """Update the status of a video being imported"""
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'video/import.html', {'video': video})


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
