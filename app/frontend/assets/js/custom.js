document.addEventListener('DOMContentLoaded', function () {
    var dropdownItems = document.querySelectorAll('.dropdown-menu .dropdown-item');

    dropdownItems.forEach(function (item) {
        item.addEventListener('click', function () {
            var parentButton = this.closest('.dropdown').querySelector('.dropdown-toggle');
            parentButton.textContent = this.textContent;
        });
    });
});


let selectedModel = 'Stable Diffusion'; // default selected model

$(document).ready(function(){
    $('.dropdown').on('hide.bs.dropdown', function (e) {
        var text = $(e.relatedTarget).text(); // Get the text of the element
        if (text) { // If the text is not empty (meaning one of the dropdown items was clicked)
            selectedModel = text; // Change selectedModel
            $('.model-button a').text(selectedModel); // Change button text
        }
    });
});

function generateRandomPrompt() {
    // Make an AJAX request to the server to get a random prompt
    fetch('/random-prompt?model=' + selectedModel, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Fill the textarea with the generated random prompt
        document.getElementById('message-1').value = data.prompt;
    })
    .catch(error => {
        console.error('Error:', error);
    });

    console.log(selectedModel);
}
