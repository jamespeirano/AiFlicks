$(document).ready(() => {
    $('.quantity__minus, .quantity__plus').click(function(e) {
        e.preventDefault();
        const input = $(this).siblings('.quantity__input');
        const value = $(this).hasClass('quantity__minus') && parseInt(input.val(), 10) > 1 ? parseInt(input.val(), 10) - 1 : parseInt(input.val(), 10) + 1;
        input.val(value);
        updateQuantityOnServer($(this).parent().data('product-id'), value);
    });
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