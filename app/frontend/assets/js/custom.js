var isTyping = false;  // Global variable to track typing status
let selectedSize = 'Medium'; // default selected model
let selectedColor = 'White'; // default selected model

function selectModel(modelName) {
    // Get the hidden input field
    let modelInput = document.getElementById('model_input');
    // Update the input field value
    modelInput.value = modelName;

    // Find the dropdown button text and update it
    let buttonText = document.querySelector('#modelButtonText');
    // Set the button text to be the selected model's text
    let updatedText = modelName.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
    buttonText.innerText = updatedText;
    // Update the selected model variable
    $('#model_input').val(text.toLowerCase().replace(' ', '-'));
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
        isTyping = false;  // Reset the typing status when done
        enableGenerateButton();  // Re-enable the button when typing is finished
    }
}

function generateRandomPrompt() {
    if (isTyping) {
        return;  // If a previous prompt is still being typed out, don't generate a new one
    }
    let selectedModel = document.getElementById('model_input').value;
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
        item.addEventListener('click', function (e) {
            // Get the clicked item text
            var text = this.textContent;

            // Update the corresponding button text
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
        var input = $(this).siblings('.quantity__input');
        var value = parseInt(input.val(), 10);
        if (value > 1) {
            value--;
        }
        input.val(value);
    });

    plus.click(function(e) {
        e.preventDefault();
        var input = $(this).siblings('.quantity__input');
        var value = parseInt(input.val(), 10);
        value++;
        input.val(value);
    });

    $('.model-item').click(function() {
        var text = $(this).text(); // Get the text of the element
        $('#modelButtonText').text(text); // Change button text
        // update the value of the hidden field with the selected model
        $('#model_input').val(text.toLowerCase().replace(' ', '-'));
    });

    $('.dropdown-item').on('click', function() {
        // Get the text of the clicked element
        var text = $(this).text();
        // Update the value of the hidden field with the selected model
        $('#model_input').val(text);
        // Update the dropdown button text
        $(this).closest('.dropdown').find('.dropdown-toggle').text(text);
    });                
});