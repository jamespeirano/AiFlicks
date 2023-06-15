let isTyping = false;

let formFields = {
    model: 'model_input',
    tsize: 'tshirtSelectedSize',
    tcolor: 'tshirtSelectedColor',
    hsize: 'hoodieSelectedSize',
    hcolor: 'hoodieSelectedColor',
};

function selectItem(fieldName, itemName) {
    updateHiddenField(fieldName, itemName);
    updateButtonText(fieldName, itemName);
}

function updateHiddenField(fieldName, itemName) {
    let input = document.getElementById(formFields[fieldName]);
    input.value = itemName;
}

function updateButtonText(fieldName, itemName) {
    let buttonId = fieldName + 'ButtonText';
    let buttonText = document.querySelector('#' + buttonId);
    let updatedText = itemName.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
    buttonText.innerText = updatedText;
}

function disableGenerateButton() {
    var generateButton = document.getElementById('generate-button');
    generateButton.disabled = true;
}

function enableGenerateButton() {
    var generateButton = document.getElementById('generate-button');
    generateButton.disabled = false;
}

function typeWriter(text, elementId, delay = 100) {
    if (text.length > 0) {
        let textarea = document.getElementById(elementId);
        textarea.value += text.charAt(0);
        text = text.slice(1);
        setTimeout(function() {
            typeWriter(text, elementId, delay);
        }, delay);
    } else {
        isTyping = false;
        enableGenerateButton();
    }
}

function generateRandomPrompt() {
    if (isTyping) {
        return;  // If a previous prompt is still being typed out, don't generate a new one
    }
    let selectedModel = document.getElementById('model_input').value;
    disableGenerateButton();
    fetch('/random-prompt?model=' + selectedModel, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message-1').value = '';
        console.log(data.prompt)
        isTyping = true;
        typeWriter(data.prompt, 'message-1', 20);
    })
    .catch(error => {
        console.error('Error:', error);
        enableGenerateButton();
    });
}

window.onload = function() {
    document.getElementById('generate-button').addEventListener('click', function() {
        var textAreaContent = document.getElementById('message-1').value;

        if (textAreaContent.trim() !== "") {
            document.getElementById("loader-overlay").style.display = "flex";
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var dropdownItems = document.querySelectorAll('.dropdown-menu .dropdown-item');

    dropdownItems.forEach(function (item) {
        item.addEventListener('click', function (e) {
            var text = this.textContent;
            var parentDropdown = this.closest('.dropdown');
            parentDropdown.querySelector('.dropdown-toggle').textContent = text;
        });
    });
});

$(document).ready(function() {
    const minus = $('.quantity__minus');
    const plus = $('.quantity__plus');

    minus.click(function(e) {
        e.preventDefault();
        let input = $(this).siblings('.quantity__input');
        let totalElement = $(this).closest('.row').find('.total-span'); 
        let originalPrice = parseFloat(totalElement.data('original-price'));
        let value = parseInt(input.val(), 10);
        if (value > 1) {
            value--;
        }
        input.val(value);

        let newPrice = originalPrice * value;
        totalElement.text(newPrice.toFixed(2));

        updateSubtotal();
    });

    plus.click(function(e) {
        e.preventDefault();
        let input = $(this).siblings('.quantity__input');
        let totalElement = $(this).closest('.row').find('.total-span'); 
        let originalPrice = parseFloat(totalElement.data('original-price'));
        let value = parseInt(input.val(), 10);
        value++;
        input.val(value);

        let newPrice = originalPrice * value;
        totalElement.text(newPrice.toFixed(2));

        updateSubtotal();
    });

    function updateSubtotal() {
        let subtotal = 0;
        $('.total-span').each(function() {
            subtotal += parseFloat($(this).text());
        });
        $('#subtotal').text(subtotal.toFixed(2));
    }

    updateSubtotal();  // Call the function as soon as the page loads.

    $('.dropdown-item').on('click', function() {
        let text = $(this).text();
        let parentDropdown = $(this).closest('.dropdown');
        
        let dropdownType = parentDropdown[0].classList[1];
        let fieldName = dropdownType.split('-')[0];
    
        // Determine if the dropdown is for a tshirt or hoodie
        let productType = parentDropdown.closest('form').find('input[name="selectedProduct"]').val();
    
        // Update the fieldName based on the product type
        if (productType === 'tshirt') {
            if (fieldName === 'size') fieldName = 'tsize';
            else if (fieldName === 'color') fieldName = 'tcolor';
        } else if (productType === 'hoodie') {
            if (fieldName === 'size') fieldName = 'hsize';
            else if (fieldName === 'color') fieldName = 'hcolor';
        }
    
        selectItem(fieldName, text);
    });

    $('#generate-button').on('click', function() {
        let textAreaContent = $('#message-1').val();
        if (textAreaContent.trim() !== "") {
            $("#loader-overlay").css("display", "flex");
        }
    });
});