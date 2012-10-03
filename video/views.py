"""Megascops core views"""

#pylint: disable=E1101

import time

from django.http import Http404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, \
        redirect, render

from models import Video
from tasks import fetch_video, encode


def index(request):
    """Homepage"""
    videos = Video.ready.all()
    return render_to_response('index.html', {'videos': videos},
            context_instance=RequestContext(request))


def video_list(request):
    """List of all videos"""
    videos = Video.ready.all()
    return render_to_response('video_list.html', {
        'videos': videos
        }, context_instance=RequestContext(request)
    )


@login_required
def importvideo(request):
    """Shown when importing a video"""
    if request.method == "POST":
        video_url = request.POST.get("url")
    else:
        raise Http404

    # Check if the video has already been downloaded
    try:
        video = Video.objects.get(page_url=video_url)
    except ObjectDoesNotExist:
        state = "DOWNLOAD_INIT"
        video = Video()
        video.profile = request.user.profile
        video.page_url = video_url
        video.state = state
        video.save()
        fetch_video.delay(video.id)
    else:
        state = video.state

    return render_to_response('import.html',
                              {'video': video},
                              context_instance=RequestContext(request))


@login_required
def refresh(request, video_id):
    """Update the status of a video being imported"""
    video = get_object_or_404(Video, pk=video_id)
    return render_to_response('import.html', {'video': video},
                              context_instance=RequestContext(request))


def convert(request, video_id):
    """Convert a video to html5 format"""
    video = get_object_or_404(Video, pk=video_id)
    video.state = "CONVERTING"
    video.save()
    encode.delay(video.id)
    return redirect("/")


def play(request, filename):
    """Show a video player for the selected video"""
    video = get_object_or_404(Video, filename=filename)
    return render_to_response('play.html', {
        'video': video
        }, context_instance=RequestContext(request)
    )


@login_required
def delete(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    # TODO : delete the files
    return render_to_response('deleted.html', {},
                              context_instance=RequestContext(request))


def livecast(request):
    """Experimental livecast"""
    timestamp = int(time.time())
    return render_to_response(
        'livecast.html', {
            'host': 'newport.strycore.com',
            'webcam_port': '8090',
            'screencast_port': '8091',
            'timestamp': timestamp
            }, context_instance=RequestContext(request)
    )


def webrtc(request):
    return render(request, "video/webrtc.html")
