from subprocess import PIPE, Popen
import os
import json
import urllib
from django_gearman.decorators import gearman_job
from django.template.defaultfilters import slugify
import megascops.settings

DATA_PATH = "/home/strider/megascops"

#@gearman_job
def fetch_video(url):
    vid_info_json, quvi_status = Popen(['quvi', url], 
                                       stdout=PIPE,
                                       stderr=PIPE).communicate()
    vid_info = json.loads(vid_info_json)
    page_title = vid_info['page_title']
    flv_url = vid_info['link'][0]['url']
    dest_file = os.path.join(
        DATA_PATH,
        slugify(vid_info['page_title']) + "." + vid_info['link'][0]['file_suffix']
    )
    urllib.urlretrieve(flv_url, dest_file)


if __name__ == "__main__":
    fetch_video("http://www.youtube.com/watch?v=nxhgP6xsrsY")


