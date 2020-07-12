/*******
 * Gthnk Images
 * Ian Dennis Miller
 */

$( document ).ready( function() {
    $("#entries img").addClass('img-fluid img-thumbnail');
    $("#entries img").click(function() {$(this).toggleClass('img-thumbnail')});
} );
