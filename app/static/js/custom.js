window.addEventListener('pageshow', (event) => {
    // If the page was loaded from the cache
    if (event.persisted) {
        // Hide the loader
        document.getElementById('loader-overlay').style.display = 'none';
    }
});

$(document).ready(function() {
    setTimeout(function() {
        $('.flashed-messages').fadeOut('slow');
    }, 3000);
});

let isTyping = false;
const generateButton = document.getElementById('generate-button');
const message = document.getElementById('message-1');
const modelInput = document.getElementById('model_input');
const loaderOverlay = document.getElementById('loader-overlay');

function toggleGenerateButton(state) {
    generateButton.disabled = state;
}

function typeWriter(text, elementId, delay) {
    if (!text.length) {
        isTyping = false;
        toggleGenerateButton(false);
        return;
    }
    message.value += text.charAt(0);
    text = text.slice(1);
    setTimeout(() => typeWriter(text, elementId, delay), delay);
}

function generateRandomPrompt() {
    if (isTyping) return;
    const selectedModel = modelInput.value;
    toggleGenerateButton(true);
    fetch(`/gallery/random-prompt?model=${selectedModel}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        message.value = '';
        isTyping = true;
        typeWriter(data.prompt, 'message-1', 10);
    })
    .catch(error => {
        console.error('Error:', error);
        toggleGenerateButton(false);
    });
}

window.onload = () => {
    generateButton.addEventListener('click', function() {
        if (message.value.trim() !== "") loaderOverlay.style.display = "flex";
    });
};