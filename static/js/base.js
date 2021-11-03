/**
* @fileOverview Base JavaScript Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */
/* globals $, bootstrap */



// On click event handler added to error information button to build modal dialog
$("#errorInformationBtn").click(function() {
  (buildInformationModal("#errorInformationBtn", "information-modal-title", null, "#informationModal", "modal-lg"));
});

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


/**
* [Function to build information modal from data attributes and javascript content array]
* @return {[modalTitle]}                     [Modal title, string]          
*/
function buildInformationModal(btnId, titleAttribute, scriptId, modalId, modalSize) {
  let modalTitleId = modalId + "Title";
  let modalContentId = modalId + "Content";
  let modalSizeId = modalId + "Size";
  // Get modal title from data atttribute
  let modalTitle = $(btnId).data(titleAttribute);
  $(modalTitleId).text(modalTitle);
  let contentHTML;
  if (scriptId) {
      // Get modal content from javascript content array if passed
      let contentArray = JSON.parse($(scriptId).text());
      // Build content HTML
      contentHTML= "<p>" + contentArray.join("</p><p>") + "</p>";

  } else {
      // Else get modal content from data attribute
      let modalContent = $(btnId).data("information-modal-content");
      // Build content HTML
      contentHTML= "<p>" + modalContent + "</p>";
  }
  // Remove size classes
  $(modalSizeId).removeClass("modal-sm");
  $(modalSizeId).removeClass("modal-lg");
  $(modalSizeId).removeClass("modal-xl");
  // Set modal size
  if ((modalSize) != "") {
      $(modalSizeId).addClass(modalSize);
  }
  // Update modal content
  $(modalContentId).html(contentHTML);
  // Show content
  $(modalId).modal('show');
  return modalTitle;
}

/**
* [Function to build confirm modal from data attributes]
* @return {[modalTitle]}                     [Modal title, string]          
*/
function buildConfirmModal(btnId, modalId) {
  let modalTitleId = modalId + "Title";
  let modalContentId = modalId + "Content";
  let modalLinkId = modalId + "Confirmed";
  // Get modal title from data atttribute
  let modalTitle = $(btnId).data("confirm-modal-title");
  $(modalTitleId).text(modalTitle);
  // Get modal content from data attribute
  let modalContent = $(btnId).data("confirm-modal-content");
  // Build content HTML
  let contentHTML= "<p>" + modalContent + "</p>";
  // Update modal content
  $(modalContentId).html(contentHTML);
  // Get modal link from data atttribute
  let modalLink = $(btnId).data("confirm-modal-link");
  // Update modal link
  $(modalLinkId).attr("href", modalLink);
  // Show content
  $(modalId).modal('show');
  return modalTitle;
}
