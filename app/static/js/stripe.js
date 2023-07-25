var stripe = Stripe('pk_test_51Mpg4OHhtpW6f5otExCngnzTqoKFajMkw4juwWvZpLUZ8fCG0wcGjS2sizkSdcExydKbfCZF3gksF2l4RAOb5uUd00trbKHsuI');

document.getElementById('subscribe-button').addEventListener('click', function(e) {
    fetch('/aiflix_user/create-checkout-session', {
        method: 'POST',
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(session) {
        return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function(result) {
        if (result.error) {
            alert(result.error.message);
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});
