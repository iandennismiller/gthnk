var mtime = 0;

function check_buffer(do_reload) {
  $.ajax({
    dataType: "json",
    url: "/day/live/latest.json",
    success: function(data) {
      if (data.timestamp > mtime) {
        mtime = data.timestamp;
        if (do_reload) {
          localStorage.setItem("do-scroll", "true");
          window.location.reload(true);
        }
      }
    }
  });
}

// check the buffer periodically
setInterval( function() {
  check_buffer(true);
}, 5000);

// check the buffer once, right now, just to set the mtime.
check_buffer(false);

if (localStorage.getItem("do-scroll") == "true") {
  localStorage.setItem("do-scroll", "false");
  window.scrollTo(0, document.body.scrollHeight);
}
