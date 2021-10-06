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

$('.basket-quantity-input').each(function () {
    let currentQuantity = parseInt($(this).val())
    let quantityInputId = "#" + $(this).attr('id')
    let quantityMinusBtnId = "#" + $(this).next().attr('id')
    let quantityPlusBtnId = "#" + $(this).next().next().attr('id')
    console.log(quantityInputId)
    console.log(quantityMinusBtnId)
    console.log(quantityPlusBtnId)
    $(quantityMinusBtnId).click(function() {
        (incrementQuantity(quantityInputId, quantityMinusBtnId, quantityPlusBtnId, -1, 1, 99));
    });
    $(quantityPlusBtnId).click(function() {
        (incrementQuantity(quantityInputId, quantityMinusBtnId, quantityPlusBtnId, 1, 1, 99));
    });
});