/**
* @fileOverview JavaScript Products Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

/* Set product rating stars for all divs with the class product-rating-stars */
/* Note - reads the product rating from the product-rating data attribute */
$('.product-rating-stars').each(function () {
    let productRating = $(this).data("product-rating")
    if ((productRating == "None") || (productRating == null) || (productRating == ""))
        $(this).html("<i class=product-rating-text>Not Rated</i>")
    else {
        let productRatingRounded = (Math.round(productRating));
        stars = $(this).children();
        stars.each(function(si) {
            if (productRatingRounded > si) {
                $(this).addClass("fg-yellow");
            }
        })
    }
});

// On click event handler added to product image link to build modal dialog
$("#productInformationImgLink" ).click(function() {
    (buildModal("#productInformationBtn", "information-modal-title", "#product-description-array", "#informationModal"));
});

// On click event handler added to product information button to build modal dialog
$("#productInformationBtn" ).click(function() {
    (buildModal("#productInformationBtn", "information-modal-title", "#product-description-array", "#informationModal"));
});

// On click event handler added to size information button to build modal dialog
$("#sizeInformationBtn" ).click(function() {
    (buildModal("#sizeInformationBtn", "information-modal-title", "#size-information-array", "#informationModal"));
});

// On click event handler added to type information button to build modal dialog
$("#typeInformationBtn" ).click(function() {
    (buildModal("#typeInformationBtn", "information-modal-title", "#type-information-array", "#informationModal"));
});

/**
* [Function to build information modal from data attributes and javascript array]
* @return {[modalTitle]}                     [Modal title, string]          
*/
function buildModal(btnId, titleAttribute, scriptId, modalId) {
    let modalTitleId = modalId + "Title";
    let modalContentId = modalId + "Content";
    $(modalTitleId).text($(btnId).data(titleAttribute));
    let contentArray = JSON.parse($(scriptId).text());
    let contentHTML= "<p>" + contentArray.join("</p><p>") + "</p>"
    $(modalContentId).html(contentHTML);
    $(modalId).modal('show')
}
