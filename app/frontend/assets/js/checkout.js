$(document).ready(function() {
    // Set Stripe key which is in .env file
    var stripe = Stripe('pk_test_51Mpg4OHhtpW6f5otExCngnzTqoKFajMkw4juwWvZpLUZ8fCG0wcGjS2sizkSdcExydKbfCZF3gksF2l4RAOb5uUd00trbKHsuI');
    const loaderOverlay = document.getElementById("loader-overlay");

    // Set up Stripe elements
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');

    // Display Stripe card errors
    card.addEventListener('change', function(event) {
        var displayError = document.getElementById('card-error');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    // Handle modal show event
    $('#paymentModal').on('show.bs.modal', function (event) {
        let subtotal = parseFloat(document.getElementById('subtotal').innerText);
    
        var button = $(event.relatedTarget);
        var recipient = subtotal.toFixed(2);
        var modal = $(this);
        modal.find('#subtotal-input').val(recipient);
    });

    // Handle form submission
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        stripe.createToken(card).then(function(result) {
            if (result.error) {
                var errorElement = document.getElementById('card-error');
                errorElement.textContent = result.error.message;
            } else {
                stripeTokenHandler(result.token);
            }
        });
    });

    function stripeTokenHandler(token) {
        let name = document.getElementById('customer-name').value;
        let email = document.getElementById('customer-email').value;
        let address = document.getElementById('customer-address').value;
        let city = document.getElementById('customer-city').value;
        let zip = document.getElementById('customer-zip').value;
        let subtotal = document.getElementById('subtotal-input').value;

        let checkoutData = {
            'name': name,
            'email': email,
            'address': address + ', ' + city + ', ' + zip,
            'subtotal': subtotal,
            'stripeToken': token.id,
        };

        fetch('/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(checkoutData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});