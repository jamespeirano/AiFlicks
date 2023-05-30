$(document).ready(function() {
    $('#prompt').on('submit', function() {
        // collect checkbox values
        var photorealistic = $('#photorealistic-checkbox').is(':checked');
        var semantic = $('#semantic-checkbox').is(':checked');
        var coherence = $('#coherence-checkbox').is(':checked');
        var novelty = $('#novelty-checkbox').is(':checked');

        // set checkbox values in hidden inputs
        $('input[name="photorealistic"]').val(photorealistic);
        $('input[name="semantic"]').val(semantic);
        $('input[name="coherence"]').val(coherence);
        $('input[name="novelty"]').val(novelty);

        // submit the form
        return true;
    });
});

function addToCart(name, price) {
    const selectElement = event.target.previousElementSibling;
    const selectedSize = selectElement.value;
    
    if (selectedSize === '') {
        alert('Please select a size.');
        return;
    }

    const overlayImage = document.querySelector(".overlay-image");
    // const overlayImageId = overlayImage.dataset_id; no longer necessary

    console.log("image ", overlayImage);
    console.log("image ", overlayImage.src);
    
    // Send an AJAX request to the backend server to add the item to the Python list
    // also add the image to the cart
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

    const data = JSON.stringify({
        'name': name,
        'price': price,
        'size': selectedSize,
        'image': overlayImage.src
    });
    xhr.send(data);
}

function generateRandomPrompt() {
    // Get the currently selected model
    const selectedModel = document.getElementById('selected-model').value;

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
        document.getElementById('prompt-textarea').value = data.prompt;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
