/**
* @fileOverview Basket JavaScript Function Library.
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
    // Add on click event handler to quantity minus button
    // Using incrementQuantity function from Products JavaScript Function Library
    $(btnMinusID).click(function() {
        (incrementQuantity(quantityInputId, btnMinusID, btnPlusID, -1, 1, 99));
    });
    // Add on click event handler to quantity plus button
    // Using incrementQuantity function from Products JavaScript Function Library
    $(btnPlusID).click(function() {
        (incrementQuantity(quantityInputId, btnMinusID, btnPlusID, 1, 1, 99));
    });
});

// Update quantity on click
$('.basket-quantity-update').click(function(e) {
    let linkId = $(this).attr('id')
    console.log(linkId)
    let form = $(this).prev('.basket-update-form');
    let formId = form.attr('id')
    console.log(formId)
    // form.submit();
})

// Remove item and reload on click
$('.basket-remove').click(function(e) {
    let csrfToken = "{{ csrf_token }}";
    let productKey = $(this).data('product-key');
    console.log(productKey)
    let url = `/bag/remove/${productKey}`;
    console.log(url)
    let data = {'csrfmiddlewaretoken': csrfToken};
    console.log(data)
    //$.post(url, data)
    //    .done(function() {
    //        location.reload();
    //   });
})
