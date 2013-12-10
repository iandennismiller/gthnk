// files was created and loaded via work_ls.json

function dateToYMD(date) {
    var d = date.getDate();
    var m = date.getMonth() + 1;
    var y = date.getFullYear();
    return '' + y + '-' + (m<=9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d);
}

var today = new Date();
var day = 60*60*24*1000;
var week = day*7;

// go through the 10 most recent
recent = data['work'].slice(0, 20);
for (var i in recent) {
    var d = new Date(recent[i][0]);
    // color code: each day the font gets lighter
    var luminance = (today - d) / day;
    var datestamp = $("<span class='time'>").html(dateToYMD(d));
    var project_name = $("<span class='name'>").html(recent[i][1]);
    var li = $("<li>").append(datestamp).append(project_name);
    var color = "hsl(0,0%," + Math.floor(luminance) + "%)";
    li.css('color', color);
    $("#recent_list").append(li);
}

/*
lists
*/

for (var i in data['lists']['ideas']) {
    var li = $("<li>").html(data['lists']['ideas'][i]);
    $("#ideas_list").append(li);
}

for (var i in data['lists']['themes']) {
    var li = $("<li>").html(data['lists']['themes'][i]);
    $("#themes_list").append(li);
}

for (var i in data['lists']['media']) {
    var li = $("<li>").html(data['lists']['media'][i]);
    $("#media_list").append(li);
}

for (var i in data['lists']['radar']) {
    var li = $("<li>").html(data['lists']['radar'][i]);
    $("#radar_list").append(li);
}

for (var i in data['lists']['wanna']) {
    var li = $("<li>").html(data['lists']['wanna'][i]);
    $("#wanna_list").append(li);
}

/*
Todos
*/

var todo_count = 0;
for (var i in data['todo']) {
    if (!data['todo'][i].completed) {
        todo_count += 1;
        var li = $("<li>").html(data['todo'][i].title);
        $("#todo_list").append(li);
    }
    if (todo_count > 15) {
        break;
    }
}

/*
Controls: make the ul inside a .ctl respond to clicks
*/

$('.ctl').click(function() {
    var elm = $(this).parent().parent().children("ul");
    elm.animate({
            height: "toggle",
            opacity: "toggle"
        });
});
