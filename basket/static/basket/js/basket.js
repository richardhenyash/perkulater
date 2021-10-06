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
    let quantityInputId = "#" + $(this).attr('id')
    let btnMinusID = "#" + $(this).next().attr('id')
    let btnPlusID = "#" + $(this).next().next().attr('id')
    let currentQuantity = parseInt($(this).val())
    console.log(currentQuantity)
    if (currentQuantity == 1){
        $(btnMinusID).attr("disabled", true)
    } else {
        $(btnMinusID).removeAttr('disabled')
    }
    if (currentQuantity == 99){
        $(btnPlusID).attr("disabled", true)
    } else {
        $(btnPlusID).removeAttr('disabled')
    }
    console.log(quantityInputId)
    console.log(btnMinusID)
    console.log(btnPlusID)
    $(btnMinusID).click(function() {
        (incrementQuantity(quantityInputId, btnMinusID, btnPlusID, -1, 1, 99));
    });
    $(btnPlusID).click(function() {
        (incrementQuantity(quantityInputId, btnMinusID, btnPlusID, 1, 1, 99));
    });
});