from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

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
        video.page_url = video_url
        video.state = state
        video.save()
        client = GearmanClient()
        t = client.dispatch_background_task('video.get_video_job', video.id)
        print t
    else:
        state = video.state

    return render_to_response('import.html',
                              {'video': video},
                              context_instance=RequestContext(request))


def convert(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    return redirect("/converting/")
