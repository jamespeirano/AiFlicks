$(document).ready(function() {
    // Set Stripe key
    var stripe = Stripe('pk_test_51Mpg4OHhtpW6f5otExCngnzTqoKFajMkw4juwWvZpLUZ8fCG0wcGjS2sizkSdcExydKbfCZF3gksF2l4RAOb5uUd00trbKHsuI');

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
        let subtotal = 0;
        document.querySelectorAll('.total-span').forEach(function(totalSpan) {
            subtotal += parseFloat(totalSpan.getAttribute('data-original-price'));
        });
        document.getElementById('subtotal').innerText = subtotal.toFixed(2);

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
        var form = document.getElementById('payment-form');
        var hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', token.id);
        form.appendChild(hiddenInput);

        form.submit();
    }
});
