/**
* @fileOverview Checkout JavaScript Function Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
// var elements = stripe.elements();

//https://stackoverflow.com/questions/43824382/custom-font-src-with-stripe/56985340

var elements = stripe.elements({
  fonts: [
    {
      // integrate Google Fonts Montserrat into stripe
      cssSrc: 'https://fonts.googleapis.com/css?family=Montserrat:400',
    }
  ]
});

var style = {
    base: {
        color: '#FAFAFA',
        fontFamily: 'Montserrat, sans-serif',  // set integrated font family
        fontSmoothing: 'antialiased',
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
var card = elements.create('card', {style: style});
card.mount('#card-element');