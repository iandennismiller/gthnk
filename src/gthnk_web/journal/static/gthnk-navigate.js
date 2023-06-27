var go_tomorrow = function() {
    if (tomorrow) {
        window.location.href = "/journal/" + tomorrow + ".html";
    } else {
        window.location.href = "/journal/live";
    }
}

var go_yesterday = function() {
    if (yesterday) {
        window.location.href = "/journal/" + yesterday + ".html";
    } else {
        window.location.href = "/journal/latest";
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
        window.location.href = "/journal/live";
    }
}

document.onkeydown = checkKey;

var swiper = new Swipe(document.getElementsByTagName('body')[0]);

// init touch swiper
swiper.onLeft(go_tomorrow);
swiper.onRight(go_yesterday);
swiper.run();
