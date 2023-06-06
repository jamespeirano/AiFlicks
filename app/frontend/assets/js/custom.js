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
    }
}

function generateRandomPrompt() {
    if (isTyping) {
        return;  // If a previous prompt is still being typed out, don't generate a new one
    }
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
        typeWriter(data.prompt, 'message-1', 40);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
