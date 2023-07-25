// Function to handle model selection popup
function handleModelSelectionPopup() {
    const modelModal = document.getElementById('modelModal');
    const modelButtons = document.querySelectorAll('.model-item');
    
    // Function to update the model name when a model button is clicked
    function updateModelName(modelName) {
        // Convert modelName to title case
        const titleCaseModelName = modelName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        const modelButtonText = document.getElementById('modelButtonText');
        modelButtonText.textContent = titleCaseModelName;
        const modelInput = document.getElementById('model_input');
        modelInput.value = modelName;
    }    

    // Add click event listeners to each model button
    modelButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            if (!button.classList.contains('disabled')) {
                const modelName = button.dataset.model;
                updateModelName(modelName);
                const modelModal = new bootstrap.Modal(document.getElementById('modelModal'));
                modelModal.hide();
            }
        });
    });
}

// Call the function to handle the model selection popup
document.addEventListener('DOMContentLoaded', () => {
    handleModelSelectionPopup();
});