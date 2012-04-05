from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django_gearman import GearmanClient, Task
from models import Video


def index(request):
    videos = Video.ready.all()
    return render_to_response('index.html', {'videos': videos},
            context_instance=RequestContext(request))


def video_list(request):
    videos = Video.ready.all()
    return render_to_response('video_list.html', {
        'videos': videos
        }, context_instance=RequestContext(request)
    )


@login_required
def importvideo(request):
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
        client = GearmanClient()
        client.dispatch_background_task('video.get_video_job', video.id)
    else:
        state = video.state

    return render_to_response('import.html',
                              {'video': video},
                              context_instance=RequestContext(request))


def convert(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.state = "CONVERTING"
    video.save()
    client = GearmanClient()
    client.dispatch_background_task('video.encode', video.id)


    return redirect("/converting/")

def play(request, filename):
    video = get_object_or_404(Video, filename=filename)
    return render_to_response('play.html', {
        'video': video 
        }, context_instance=RequestContext(request)
    )
    
