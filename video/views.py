from django.shortcuts import render_to_response
from django.template import RequestContext
from gearman import GearmanClient

from django.conf import settings

try:
    import cPickle as pickle
except ImportError:
    import pickle

def index(request):
    return render_to_response('index.html', {
            
        }, context_instance=RequestContext(request)
    )
    

def importvideo(request):
    if request.method == "POST":
        video_url = request.POST.get("url")
    return render_to_response('import.html', {
            
        }, context_instance=RequestContext(request)
    )
    



