"""Megascops core views"""
#pylint: disable=E1101
import time

from django.contrib.auth.models import User
from django.http import Http404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import (render_to_response, get_object_or_404,
                              redirect, render)

from models import Video, Profile
from tasks import fetch_video, encode_task


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
    encode_task.delay(video.id)
    return redirect("/")


def play(request, filename):
    """Show a video player for the selected video"""
    video = get_object_or_404(Video, filename=filename)
    return render(request, 'play.html', {
        'video': video
    })


@login_required
def delete(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    return render(request, 'deleted.html')


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, _created = Profile.objects.get_or_create(user=user)
    return render(request, 'user_profile.html', {'user_profile': user_profile})


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
