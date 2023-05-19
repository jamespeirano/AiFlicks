
$(document).ready(function() {
    $('#prompt').on('submit', function() {
        // Collect checkbox values
        var photorealistic = $('#photorealistic-checkbox').is(':checked');
        var semantic = $('#semantic-checkbox').is(':checked');
        var coherence = $('#coherence-checkbox').is(':checked');
        var novelty = $('#novelty-checkbox').is(':checked');

        // Set checkbox values in hidden inputs
        $('input[name="photorealistic"]').val(photorealistic);
        $('input[name="semantic"]').val(semantic);
        $('input[name="coherence"]').val(coherence);
        $('input[name="novelty"]').val(novelty);

        // Submit the form
        return true;
    });
});

function generateRandomPrompt() {
    // Make an API call to retrieve a random prompt
    fetch('/random-prompt', {
        headers : {
            'Accept-Encoding': '*'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to retrieve random prompt');
            }
            return response.json();
        })
        .then(data => {
            // Fill the textarea with the generated random prompt
            document.getElementById('prompt-textarea').value = data.prompt;
        })
        .catch(error => {
            console.log(error);
            // Handle the error appropriately (e.g., show an error message)
        });
}


function addToCart(name, price) {
    const selectElement = event.target.previousElementSibling;
    const selectedSize = selectElement.value;
    
    if (selectedSize === '') {
        alert('Please select a size.');
        return;
    }
    
    // Send an AJAX request to the backend server to add the item to the Python list
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/add-to-cart');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert(`Item "${name}" (Size: ${selectedSize}) added to the cart!`);
        } else {
            alert('Failed to add item to the cart. Please try again.');
        }
    };
    const data = JSON.stringify({ name: name, price: price, size: selectedSize });
    xhr.send(data);
}
