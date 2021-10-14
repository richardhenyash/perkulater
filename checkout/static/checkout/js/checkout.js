/**
* @fileOverview Checkout JavaScript Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

// Accepting a payment in Stripe: https://stripe.com/docs/payments/accept-a-payment
// Stripe.js and Stripe elements: https://stripe.com/docs/stripe-js
// Using google fonts with stripe: https://stackoverflow.com/questions/43824382/custom-font-src-with-stripe/56985340

let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements({
  fonts: [
    {
      // integrate Google Fonts Montserrat into stripe
      cssSrc: 'https://fonts.googleapis.com/css?family=Montserrat:400,500,600',
    }
  ]
});
let style = {
    base: {
        color: '#FAFAFA',
        fontFamily: 'Montserrat, sans-serif',  // set integrated font family
        fontSmoothing: 'antialiased',
        fontWeight: '500',
        fontSize: '14px',
        '::placeholder': {
          color: '#FAFAFA'
        }
    },
    invalid: {
        color: '#FFAD99',
        iconColor: '#FFAD99'
    }
};
let card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
            <p><span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span></p>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
let form = document.getElementById('payment-form');
form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loader-overlay').fadeToggle(100);

    let saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    let url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.address_1.value),
                        line2: $.trim(form.address_2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.address_1.value),
                    line2: $.trim(form.address_2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                }
            },
        }).then(function (result) {
            if (result.error) {
                let errorDiv = document.getElementById('card-errors');
                let html = `
                <p><span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span></p>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loader-overlay').fadeToggle(100);
                card.update({
                    'disabled': false
                });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // reload the page - the error will be in django messages
        location.reload();
    })
});
