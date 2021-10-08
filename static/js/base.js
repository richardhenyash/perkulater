/**
* @fileOverview Base JavaScript Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

/* Show Toast Messages */
$(document).ready(function(){
    $('.toast').show();
});

/* Hide toast Messages on click of close button */
$('.toast-close').each(function() {
    $(this).click(function() {
        $('.toast').hide();
    });
});
