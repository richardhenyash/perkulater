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
        $(this).html("<i>Not Rated</i>")
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
