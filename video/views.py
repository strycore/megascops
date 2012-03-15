from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django_gearman import GearmanClient, Task
from models import Video

def index(request):
    return render_to_response('index.html', { },
            context_instance=RequestContext(request))


def video_list(request):
    videos = Video.objects.all();
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
        client.dispatch_background_task('megascops.get_video_job', video.id)
    else:
        state = video.state

    return render_to_response('import.html',
                              {'video': video},
                              context_instance=RequestContext(request))
