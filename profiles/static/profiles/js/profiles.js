/**
* @fileOverview Profiles JavaScript Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

/* Set country selector to correct placeholder colour if not selected */
/* Note - setSelectColour function is located in base.js */
$( document ).ready(function() {
    setSelectColour('#id_country', 'var(--whitehighlight)', 'var(--white)');
});

/* Change event handler added to country selector */
$('#id_country').change(function() {
    setSelectColour('#id_country', 'var(--whitehighlight)', 'var(--white)');
});
