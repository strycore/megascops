timer_id = false

refresh_video_status = (video_id) ->
    $("#video-monitor-container").load "/refresh/"+video_id+"/ #video-monitor"
    return true

progress_box = $('#video-monitor').get(0)
if progress_box
    video_id = $(progress_box).attr('data-video-id')
    timer_id = window.setInterval refresh_video_status, 5000, video_id


this.launchImport = () ->
  console.log("plop")

