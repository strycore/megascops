var processor = {
  timerCallback: function() {
    this.computeFrame();
    var self = this;
    setTimeout(function () {
        self.timerCallback();
      }, 0);
  },
  doLoad: function() {
    this.screencast = document.getElementById("screencast");
    this.webcam = document.getElementById("webcam");
    this.livecast = document.getElementById("livecast");
    this.livecastContext = this.livecast.getContext("2d");
    var self = this;
    this.screencast.addEventListener("canplay", function() {
        self.width = self.screencast.videoWidth;
        self.height = self.screencast.videoHeight;
        self.camwidth = self.webcam.videoWidth;
        self.camheight = self.webcam.videoHeight;
        self.timerCallback();
      }, false);
  },
  computeFrame: function() {
    offset = 20;
    this.livecastContext.clearRect(0, 0, this.width, this.height);
    try {
      this.livecastContext.drawImage(this.screencast, 0, 0, this.width, this.height);
      this.livecastContext.drawImage(
            this.webcam,
            this.width - this.camwidth - offset,
            this.height -this.camheight - offset, 
            this.camwidth, this.camheight);
    } catch(e) {
      return;
    }
  }
};

$(document).ready(function () {
    $('#change-stream').click(function (e) {
        e.preventDefault();
        var screencast_url = $("#livecast-input").val();
        console.log(screencast_url);
        console.log($('#screencast').attr('src'));
        $("#screencast").attr('src', screencast_url);
        $("#screencast").attr('width', '640');
        $("#screencast").attr('height', '480');
    });
})
