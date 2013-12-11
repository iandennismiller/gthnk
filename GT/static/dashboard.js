// files was created and loaded via work_ls.json

function dateToYMD(date) {
    var d = date.getDate();
    var m = date.getMonth() + 1;
    var y = date.getFullYear();
    return '' + y + '-' + (m<=9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d);
}

function create_recent_work() {
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
        var project_str = recent[i][1];
        var project_name = $("<span class='name'>").html(project_str);
        var desc = $("<a href='/project/" + project_str + "'>").append(project_name).append("</a>");
        var li = $("<li>").append(datestamp).append(desc);
        var color = "hsl(0,0%," + Math.floor(luminance) + "%)";
        li.css('color', color);
        $("#recent_list").append(li);
    }
}

/*
lists
*/

function create_lists() {
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

    for (var i in data['lists']['log']) {
        var li = $("<p>").html(data['lists']['log'][i]);
        $("#log .expando").append(li);
    }

    $("#yesterday_content").html(markdown.toHTML(data['lists']['yesterday']));
}

/*
Todos
*/

function create_todo() {
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
}

/*
Controls: make the ul inside a .ctl respond to clicks
*/

function button_controls() {
    $('.ctl').click(function() {
        $(".expando").hide();
        $("h2").removeClass("selected");
        $(this).addClass("selected");

        var id_name = $(this).text();
        elm = $("#" + id_name + " .expando");
        elm.show();
    });
}

function main() {
    create_recent_work();
    create_todo();
    create_lists();
    button_controls();
    $("#spinner").fadeOut();
    $("#recent .expando").fadeIn();
}

$(document).ready(main);
