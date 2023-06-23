document.getElementById('checkout-btn').addEventListener('click', function(e) {
    var stripe = Stripe('pk_test_51NK8LNDA73T5T7kqn3CqboCe93PRzJs4EtqaE6SzWekFTsGNuMim78n9Y46m2mEFZVZESI5Ng6KSx28OsoHOnAkT00G9Ug01tz');
    // Prevent default button behavior
    e.preventDefault();

    fetch('/create_checkout_session', {
        method: 'POST',
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(session) {
        return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function(result) {
        // If redirectToCheckout fails due to a browser or network
        // error, display the localized error message to your customer
        // using `result.error.message`.
        if (result.error) {
            alert(result.error.message);
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});