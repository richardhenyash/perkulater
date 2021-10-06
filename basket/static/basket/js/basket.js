/**
* @fileOverview JavaScript Basket Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */


// On click event handler added to minus button to decrease product quantity and update price
$("#basket-quantity-minus-btn").click(function() {
    (incrementQuantity("#basket-quantity", "#basket-quantity-minus-btn", "#basket-quantity-plus-btn", -1, 1, 99));
});

// On click event handler added to plus button to decrease product quantity and update price
$("#basket-quantity-plus-btn").click(function() {
    (incrementQuantity("#basket-quantity", "#basket-quantity-minus-btn", "#basket-quantity-plus-btn", 1, 1, 99));
});
