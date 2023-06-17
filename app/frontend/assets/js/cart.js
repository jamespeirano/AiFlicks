$(document).ready(() => {
    $('.quantity__minus, .quantity__plus').click(function(e) {
        e.preventDefault();
        const input = $(this).siblings('.quantity__input');
        let value = parseInt(input.val(), 10);
        if ($(this).hasClass('quantity__minus') && value > 1) {
            value -= 1;
        } else if ($(this).hasClass('quantity__plus')) {
            value += 1;
        }
        input.val(value);
        updateQuantityOnServer($(this).parent().data('product-id'), value);
    });

    let subtotal = parseFloat($('#subtotal').text());
    if(subtotal > 0){
        // Enable the button if subtotal is greater than 0
        $('#checkout-btn').prop('disabled', false);
    }
    else{
        // Disable the button if subtotal is 0
        $('#checkout-btn').prop('disabled', true);
    }
});

function updateQuantityOnServer(productId, quantity) {
    $.ajax({
        url: '/update-cart-quantity',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            productId,
            newQuantity: quantity
        }),
        success: function(response) {
            if(response.success) {
                $(`.product-total[data-product-id=${productId}]`).text(response.newTotal.toFixed(2));
                const subtotal = [...$('.product-total')].reduce((acc, cur) => acc + parseFloat($(cur).text()), 0);
                $('#subtotal').text(subtotal.toFixed(2));
            } else {
                console.error(response.error);
            }
        },
        error: console.error
    });
}