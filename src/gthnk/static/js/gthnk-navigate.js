var go_tomorrow = function() {
    if (tomorrow) {
        window.location.href = "/day/" + tomorrow + ".html";
    } else {
        window.location.href = "/day/live";
    }
}

var go_yesterday = function() {
    if (yesterday) {
        window.location.href = "/day/" + yesterday + ".html";
    } else {
        window.location.href = "/latest";
    }
}

// <!-- keyboard handler -->
function checkKey(e) {
    e = e || window.event;

    if (e.keyCode == '37') {
        go_yesterday();
    }
    else if (e.keyCode == '39') {
        go_tomorrow();
    }
    else if (e.keyCode == 192) { 
        window.location.href = "/day/live";
    }
}

// http://www.daterangepicker.com/
// 1.3.15
// https://github.com/dangrossman/bootstrap-daterangepicker/tree/0d7f4f26618e09ba6d2488a7e42273fd2fb07ae7

$('a#calendar_button').daterangepicker(
    {
        format: 'YYYY-MM-DD',
        singleDatePicker: true,
        startDate: moment(today) // set this value in the html body, within script tags
    },
    function(start, end, label) {
        window.location = "/nearest/" + start.format('YYYY-MM-DD');
    }
);

document.onkeydown = checkKey;

var swiper = new Swipe(document.getElementsByTagName('body')[0]);

// init touch swiper
swiper.onLeft(go_tomorrow);
swiper.onRight(go_yesterday);
swiper.run();
