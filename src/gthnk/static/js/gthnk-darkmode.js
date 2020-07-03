/*******
 * Gthnk Main
 * Ian Dennis Miller
 */

/******
 * Main
 */

// $( document ).ready( function() {
//     set_darkmode(localStorage.getItem("dark-mode"));
// } );

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
