/**
* @fileOverview JavaScript Basket Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

// On click event handler added to basket quantity minus and plus buttons to increase or decrease product quantity
$('.basket-quantity-input').each(function () {
    // Get input and button id's
    let quantityInputId = "#" + $(this).attr('id')
    let btnMinusID = "#" + $(this).next().attr('id')
    let btnPlusID = "#" + $(this).next().next().attr('id')
    // Disable minus button if current quantity is 1
    let currentQuantity = parseInt($(this).val())
    if (currentQuantity == 1){
        $(btnMinusID).attr("disabled", true)
    } else {
        $(btnMinusID).removeAttr('disabled')
    }
    // Disable plus button if current quantity is 99
    if (currentQuantity == 99){
        $(btnPlusID).attr("disabled", true)
    } else {
        $(btnPlusID).removeAttr('disabled')
    }
    $(btnMinusID).click(function() {
        (incrementQuantity(quantityInputId, btnMinusID, btnPlusID, -1, 1, 99));
    });
    $(btnPlusID).click(function() {
        (incrementQuantity(quantityInputId, btnMinusID, btnPlusID, 1, 1, 99));
    });
});