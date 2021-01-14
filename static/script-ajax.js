const button = document.querySelector('#buy');
const button2 = document.querySelector('#buy2');
const button3 = document.querySelector('#buy3');
button.addEventListener('click', event=>{
    fetch('/stripe_pay')
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            // Make the id field from the Checkout Session creation API response
            // available to this file, so you can provide it as parameter here
            // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, display the localized error message to your customer
            // using `result.error.message`.
        });
    })
});

button2.addEventListener('click', event=>{
    fetch('/stripe_pay')
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            // Make the id field from the Checkout Session creation API response
            // available to this file, so you can provide it as parameter here
            // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, display the localized error message to your customer
            // using `result.error.message`.
        });
    })
});

button3.addEventListener('click', event=>{
    fetch('/stripe_pay')
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            // Make the id field from the Checkout Session creation API response
            // available to this file, so you can provide it as parameter here
            // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, display the localized error message to your customer
            // using `result.error.message`.
        });
    })
});