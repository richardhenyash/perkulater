/**
* @fileOverview Base JavaScript Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */
/* globals $, bootstrap */

/* Show Toast Messages */
/* Thanks to help from Shaun at code instutute, https://getbootstrap.com/docs/5.0/components/toasts/#usage */
/* and https://stackoverflow.com/questions/63515279/how-to-initialize-toasts-with-javascript-in-bootstrap-5 */

let toastElList = [].slice.call(document.querySelectorAll('.toast'));
let toastList = toastElList.map(function (toastEl) {
    /* Set toast initialisation options */
    let option = {
        animation: true,
        autohide: false,
        delay: 5000,
    };
  let bsToast = new bootstrap.Toast(toastEl, option);
  /* Show toasts */
  bsToast.show();
});

/**
* [Function to set the correct colour on a select element
* @return {[modalTitle]}                     [Modal title, string]          
*/
function setSelectColour(selectId, unSelectedColour, selectedColour) {
  let selectSelected = $(selectId).val();
  let returnColour;
  if(!selectSelected) {
      returnColour = unSelectedColour;
      $(selectId).css('color', unSelectedColour);
  } else {
      returnColour = selectedColour;
      $(selectId).css('color', selectedColour);
  }
  return returnColour;
}
