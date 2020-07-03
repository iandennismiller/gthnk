var go_tomorrow = function() {
    if (tomorrow) {
        window.location.href = "/day/" + tomorrow + ".html";
    } else {
        window.location.href = "/buffer";
    }
}

var go_yesterday = function() {
    if (yesterday) {
        window.location.href = "/day/" + yesterday + ".html";
    } else {
        window.location.href = "/latest";
    }
}

// <!-- toast notifications -->

$('.toast').toast({autohide: false});
$('.toast').toast('show');

// <!-- dark mode -->

// run dark mode again to ensure the index image is correct
set_darkmode(localStorage.getItem("dark-mode"));

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
        window.location.href = "/buffer";
    }
}
document.onkeydown = checkKey;
