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
$("#productInformationImgLink").click(function() {
    (buildModal("#productInformationImgLink", "information-modal-title", "#product-description-array", "#informationModal", "modal-lg"));
});

// On click event handler added to product information button to build modal dialog
$("#productInformationBtn").click(function() {
    (buildModal("#productInformationBtn", "information-modal-title", "#product-description-array", "#informationModal", "modal-xl"));
});

// On click event handler added to size information button to build modal dialog
$("#sizeInformationBtn").click(function() {
    (buildModal("#sizeInformationBtn", "information-modal-title", "#size-information-array", "#informationModal", "modal-sm"));
});

// On click event handler added to type information button to build modal dialog
$("#typeInformationBtn").click(function() {
    (buildModal("#typeInformationBtn", "information-modal-title", "#type-information-array", "#informationModal", ""));
});

// On click event handler added to minus button to decrease product quantity
$("#product-quantity-minus-btn").click(function() {
    (incrementQuantity("#product-quantity", "#product-quantity-minus-btn", "#product-quantity-plus-btn", -1, 1, 99));
});

// On click event handler added to plus button to decrease product quantity
$("#product-quantity-plus-btn").click(function() {
    (incrementQuantity("#product-quantity", "#product-quantity-minus-btn", "#product-quantity-plus-btn", 1, 1, 99));
});

/**
* [Function to build information modal from data attributes and javascript content array]
* @return {[modalTitle]}                     [Modal title, string]          
*/
function buildModal(btnId, titleAttribute, scriptId, modalId, modalSize) {
    let modalTitleId = modalId + "Title";
    let modalContentId = modalId + "Content";
    let modalSizeId = modalId + "Size";
    // Get modal title from data atttribute
    let modalTitle = $(btnId).data(titleAttribute)
    $(modalTitleId).text(modalTitle);
    // Get modal content from javascript content array
    let contentArray = JSON.parse($(scriptId).text());
    // Build content HTML
    let contentHTML= "<p>" + contentArray.join("</p><p>") + "</p>"
    // Remove size classes
    $(modalSizeId).removeClass("modal-sm")
    $(modalSizeId).removeClass("modal-lg")
    $(modalSizeId).removeClass("modal-xl")
    // Set modal size
    if ((modalSize) != "") {
        $(modalSizeId).addClass(modalSize)
    }
    // Update modal content
    $(modalContentId).html(contentHTML);
    // Show content
    $(modalId).modal('show')
    return modalTitle
}

/**
* [Function to increment product quantities given quantityId, positive or negative increment, minimum value and mximum value]
* @return {[newQuantity]}                     [New Quantity, string]          
*/
function incrementQuantity(quantityId, btnMinusID, btnPlusID, inc, minValue, maxValue){
    let currentQuantity = parseInt($(quantityId).val())
    let newQuantity = currentQuantity
    if (Math.sign(inc) == 1) {
        if ((currentQuantity + inc) <= maxValue) {
            newQuantity = currentQuantity + inc
        }
    } else {
        if ((currentQuantity + inc) >= minValue) {
            newQuantity = currentQuantity + inc
        }            
    }
    if (newQuantity != currentQuantity) {
        $(quantityId).val(newQuantity)
    }
    if (newQuantity <= minValue) {
        $(btnMinusID).attr("disabled", true)
    } else {
        $(btnMinusID).removeAttr('disabled')
    }
    if (newQuantity >= maxValue) {
        $(btnPlusID).attr("disabled", true)
    } else {
        $(btnPlusID).removeAttr('disabled')
    }
    return newQuantity
}
