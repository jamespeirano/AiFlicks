window.onload = function() {
    document.getElementById('generate-button').addEventListener('click', function() {
        var textAreaContent = document.getElementById('message-1').value;

        if (textAreaContent.trim() !== "") { // if the textarea is not empty
            document.getElementById("loader-overlay").style.display = "flex";
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var dropdownItems = document.querySelectorAll('.dropdown-menu .dropdown-item');

    dropdownItems.forEach(function (item) {
        item.addEventListener('click', function () {
            var parentButton = this.closest('.dropdown').querySelector('.dropdown-toggle');
            parentButton.textContent = this.textContent;
        });
    });
});

function selectModel(modelName) {
    // Get the hidden input field
    let modelInput = document.getElementById('model_input');
    // Update the input field value
    modelInput.value = modelName;
}

var isTyping = false;  // Global variable to track typing status

function typeWriter(text, elementId, delay = 100) {
    if (text.length > 0) {
        let textarea = document.getElementById(elementId);
        textarea.value += text.charAt(0);
        text = text.slice(1);
        setTimeout(function() {
            typeWriter(text, elementId, delay);
        }, delay);
    } else {
        isTyping = false;  // Reset the typing status when done
        enableGenerateButton();  // Re-enable the button when typing is finished
    }
}

function disableGenerateButton() {
    var generateButton = document.getElementById('generate-button');
    generateButton.disabled = true;
}

function enableGenerateButton() {
    var generateButton = document.getElementById('generate-button');
    generateButton.disabled = false;
}

function generateRandomPrompt() {
    if (isTyping) {
        return;  // If a previous prompt is still being typed out, don't generate a new one
    }
    disableGenerateButton();  // Disable the button while generating the prompt
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
        isTyping = true;  // Set the typing status before starting to type
        typeWriter(data.prompt, 'message-1', 20);
    })
    .catch(error => {
        console.error('Error:', error);
        enableGenerateButton();  // Re-enable the button in case of an error
    });
}

// Function to add the base64 image to the cart page
function addImageToCartPage(base64Image) {
    // Find the image element on the cart page and update its source
    let cartImageElement = document.getElementById('cart-image');
    cartImageElement.src = 'data:image/png;base64,' + base64Image;
}

async function addToCart(event) {
    event.preventDefault(); // Prevent the default link click behavior

    // Get the base64 image
    let base64Image = document.querySelector('.generated-image img').src.split(",")[1];

    // Add the product to the cart
    let product_id = document.querySelector("[data-reflow-product]").getAttribute("data-reflow-product");
    let variant_id = document.querySelector(".ref-field-variants").value;
    let quantity = document.querySelector(".ref-quantity-widget input").value;

    addToCartWithProductId(product_id, variant_id, quantity);

    // Add the image to the cart page
    addImageToCartPage(base64Image);
}

// Function to add the product to the cart using Reflow API
function addToCartWithProductId(productId, variantId, quantity) {
    fetch(`https://api.reflowhq.com/v1/stores/1688931258/cart/items`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 74623a7.8aac0589da35e819d0a87843debee5'
        },
        body: JSON.stringify({
            product_id: productId,
            variant_id: variantId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response and perform any necessary actions
        console.log("Product added to cart:", data);
        // Redirect to the shopping cart page
        window.location.href = "cart.html";
    })
    .catch(error => {
        // Handle any errors that occur during the API request
        console.error("Error adding product to cart:", error);
    });
}

window.addEventListener('load', (event) => {
    // Find the product name element on the cart page and update its text
    let cartProductNameElement = document.querySelector('.cart-product-name');
    if (cartProductNameElement) {
        cartProductNameElement.textContent = 'Good Product';
    }
});


let selectedModel = 'stable-diffusion'; // default selected model
$(document).ready(function(){
    $('.dropdown').on('hide.bs.dropdown', function (e) {
        var text = $(e.relatedTarget).text(); // Get the text of the element
        if (text) { // If the text is not empty (meaning one of the dropdown items was clicked)
            selectedModel = text.toLowerCase().replace(/ /g, '-'); // Change selectedModel and convert to lowercase with spaces replaced with dashes
            $('.model-button a').text(text); // Change button text (use original text here)
        }
    });
});

document.getElementById("modelDropdown").addEventListener("change", function() {
    // Update the value of the hidden field with the selected model
    document.getElementById("model").value = this.value;
});