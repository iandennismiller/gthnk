var today = null;
var yesterday = null;
var tomorrow = null;
var live_page = null;

function get_day_json(date_str) {
    var url = "/journal/" + date_str + ".json";
    return $.ajax({
        dataType: "json",
        url: url,
        async: false
    });
}

function disable_button(id) {
    $(id).addClass("disabled");
    $(id).removeClass("text-white");
}

function enable_button(id) {
    $(id).removeClass("disabled");
    $(id).addClass("text-white");
}

async function update_day(date_str) {
    var _json = await get_day_json(date_str);
    today = _json["datestamp"];
    tomorrow = _json["tomorrow"];
    yesterday = _json["yesterday"];

    $("#day-of-week").text(_json["day_of_week"]);
    $("#entries").html(_json["content"]);

    if (!tomorrow) {
        disable_button("#link-tomorrow");
    } else {
        enable_button("#link-tomorrow");
    }

    if (!yesterday) {
        disable_button("#link-yesterday");
    } else {
        enable_button("#link-yesterday");
    }

    if (date_str == "live") {
        disable_button("#link-live");
        live_page = true;
        window.scrollTo(0, document.body.scrollHeight);
        start_checking_status();
    } else {
        enable_button("#link-live");
        live_page = false;
        stop_checking_status();
    }

    window.history.pushState({}, date_str, url="/journal/" + date_str + ".html");
}

function go_to_yesterday() {
    if (yesterday) {
        // window.history.pushState({}, yesterday, url="/journal/" + yesterday + ".html");
        update_day(yesterday);
    } else {
        window.location.href = "/journal/latest";
    }
}

function go_to_tomorrow() {
    if (tomorrow) {
        // window.history.pushState({}, tomorrow, url="/journal/" + tomorrow + ".html");
        update_day(tomorrow);
    } else {
        if (!live_page) {
            // window.history.pushState({}, tomorrow, url="/journal/live.html");
            update_day("live");
        }
    }
}

function checkKey(e) {
    e = e || window.event;

    if (e.keyCode == '37') {
        go_to_yesterday();
    }
    else if (e.keyCode == '39') {
        go_to_tomorrow();
    }
    else if (e.keyCode == 192) { 
        window.location.href = "/journal/live";
    }
}

// mtime for status checking
var mtime = 0;

// timer for the status checker
var status_checker = null;

function check_buffer() {
    $.ajax({
        dataType: "json",
        url: "/journal/status.json",
        success: function(data) {
            if (data.timestamp > mtime) {
                mtime = data.timestamp;
                update_day("live"); 
            } else {
                if (yesterday != data.latest) {
                    update_day("live");
                }
            }
        }
    });
}

function start_checking_status() {
    if (!status_checker) {
        status_checker = setInterval( function() {
            check_buffer();
        }, 5000);

        // check the buffer once, right now, just to set the mtime.
        check_buffer();
    }
}

function stop_checking_status() {
    if (status_checker) {
        clearInterval(status_checker);
        status_checker = null;
    }
}

// init keyboard handling
document.onkeydown = checkKey;

// init touch swiper
var swiper = new Swipe(document.getElementsByTagName('body')[0]);
swiper.onLeft(go_to_tomorrow);
swiper.onRight(go_to_yesterday);
swiper.run();
