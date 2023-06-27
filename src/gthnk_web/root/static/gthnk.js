// <!-- toast notifications -->

$('.toast').toast({autohide: false});
$('.toast').toast('show');

// http://www.daterangepicker.com/
// 1.3.15
// https://github.com/dangrossman/bootstrap-daterangepicker/tree/0d7f4f26618e09ba6d2488a7e42273fd2fb07ae7

if (typeof(today) == 'undefined') {
    var picker_date = new Date();
}
else {
    var picker_date = moment(today); // set this value in the html body, within script tags
}

$('a#calendar_button').daterangepicker(
    {
        "format": 'YYYY-MM-DD',
        "singleDatePicker": true,
        "showDropdowns": true,
        "autoApply": true,
        "opens": "left",
        "startDate": picker_date
    },
    function(start, end, label) {
        window.location = "/journal/nearest/" + start.format('YYYY-MM-DD');
    }
);

/**********
 * dark mode
 */

var set_darkmode = function(to_dark) {
    if (to_dark == "on") {
      $("body").removeClass("bootstrap").addClass("bootstrap-dark");
      $("#gthnk-logo").attr('src', "/static/gthnk-logo-dark.png");
      localStorage.setItem("dark-mode", "on");
    }
    else {
      $("body").removeClass("bootstrap-dark").addClass("bootstrap");
      $("#gthnk-logo").attr('src', "/static/gthnk-logo.png");
      localStorage.setItem("dark-mode", "off");
    }
  }
  
var toggle_darkmode = function() {
    if (localStorage.getItem("dark-mode") == "on") {
        set_darkmode("off");
    }
    else {
        set_darkmode("on");
    }
}

// run immediately to prevent flicker
set_darkmode(localStorage.getItem("dark-mode"));
