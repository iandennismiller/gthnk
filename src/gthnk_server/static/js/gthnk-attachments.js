/*******
 * Gthnk UI
 * Ian Dennis Miller
 */

var set_height = function(){
    $("#entries_scroller").css("height", $(window).height()-56);
    $("#pages_scroller").css("height", $(window).height()-80);
    $("#page_wrapper").css("height", $(window).height()-56-50);
}

/**********
 * Handlers
 */

// $(window).resize( set_height );

// http://stackoverflow.com/questions/4198041/jquery-smooth-scroll-to-an-anchor/12714767#12714767
$(".scroll").click(function(event){
    event.preventDefault();
    window.history.replaceState(null, this.title, url=this.hash);
    var dest=$('#entries_scroller').scrollTop()+($(this.hash).offset().top)-60;
    $('#entries_scroller').animate({scrollTop:dest}, 300,'swing');
 });

$(".top_of_page").click(function(event){
    $('#pages_scroller').animate({scrollTop:100}, 300,'swing');
})

$("#entries, .image_container").hover(
    function() {
        if (!$("body").hasClass("editing")) {
            $(this).find('.controllable .viewable').fadeIn();
        }
    },
    function() {
        if (!$("body").hasClass("editing")) {
            $(this).find('.controllable .viewable').fadeOut();
        }
    }
);

$("#edit_button").click(function() {
    $("body").toggleClass("editing");
    $("#edit_button").toggleClass("active");

    if ($("body").hasClass("editing")) {
        $('.controllable .editable').fadeIn();
    }
    else {
        $('.controllable .editable').fadeOut();
    }
});

$(".viewable a").click(function(){
    window.history.replaceState(null, this.title, url="#"+$(this).attr("anchorid"));
});

$(".delete_button").click(function() {
    var container = $(this).parent().children()[1];
    console.log(container);
    $(container).toggle("slide");
});

$(".cancel_button").click(function() {
    var container = $(this).parent();
    console.log(container);
    $(container).toggle("slide");
});

var set_image_widths = function() {
    // set image widths
    var widths = $(".page_attachment a + div img").map(function(){
        return $(this).width();
    }).get();

    $(".image_container").each(function(index, value){
        $(value).css("width", widths[index]);
    });
}

// $(window).bind("load", function() {
//     set_image_widths();
// });

/******
 * Main
 */

$( document ).ready( function() {
    // set_height();
    // $('#pages_scroller').scrollTop(100);

    // $('.controllable .editable').hide();
    // $('.controllable .viewable').hide();

    /*$("img.lazy").lazy({
        appendScroll: $("div.image_container")
    });*/
} );
