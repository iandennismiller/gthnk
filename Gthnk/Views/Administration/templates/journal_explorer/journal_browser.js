    // http://stackoverflow.com/questions/4198041/jquery-smooth-scroll-to-an-anchor/12714767#12714767
    $(".scroll").click(function(event){
        event.preventDefault();
        var dest=$('#entries_scroller').scrollTop()+($(this.hash).offset().top)-60;
        $('#entries_scroller').animate({scrollTop:dest}, 300,'swing');
     });

    $(".top_of_page").click(function(event){
        $('#pages_scroller').animate({scrollTop:100}, 300,'swing');
    })

    var set_height = function(){
        $("#entries_scroller").css("height", $(window).height()-99);
        $("#pages_scroller").css("height", $(window).height()-57);
        $("#page_wrapper").css("height", $(window).height()+50);
    }

    $("#edit_button").click(function() {
        $("body").toggleClass("editing");
        //$(".controllable .viewable").toggleClass("off");
        //$(".controllable .editable").toggleClass("off");
        //$(".controllable").toggleClass("visible");
        $("#edit_button").toggleClass("active");

        if ($("body").hasClass("editing")) {
            $('.controllable .editable').fadeIn();
            //$('.controllable').fadeIn();
        }
        else {
            //$('.controllable .viewable').css("opacity", 0);
            //$('.controllable').fadeOut();
            $('.controllable .editable').fadeOut();
            //$('.controllable').fadeOut();
        }

    })

    $( window ).resize( set_height );

    reveal_confirm_widget = function() {
        var container = $(this).parent().children()[1];
        console.log(container);
        $(container).toggle("slide");
    }

    hide_confirm_widget = function() {
        var container = $(this).parent();
        console.log(container);
        $(container).toggle("slide");
    }

    set_image_widths = function() {
        // set image widths
        var widths = $(".page_attachment a + div img").map(function(){
            return $(this).width();
        }).get();

        $(".image_container").each(function(index, value){
            $(value).css("width", widths[index]);
        });
    }

    $( document ).ready( function() {
        set_height();
        $('#pages_scroller').scrollTop(100);
        $(".delete_button").click(reveal_confirm_widget);
        $(".cancel_button").click(hide_confirm_widget);
        $('.controllable .editable').hide();
        $('.controllable .viewable').hide();

        /*$("img.lazy").lazy({
            appendScroll: $("div.image_container")
        });*/
    } );

    $(window).bind("load", function() {
        set_image_widths();
    });

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

