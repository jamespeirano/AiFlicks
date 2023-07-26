// Show loader
document.getElementById('loader-overlay').style.display = 'block'; 

// Start image generation after brief delay
setTimeout(function() {
  // Submit form 
  document.getElementById('prompt_form').submit();
}, 300);

function showLoader() {
    return new Promise(resolve => {
      document.getElementById('loader-overlay').style.display = 'block';
      setTimeout(resolve, 300); 
    });
  }
  
  showLoader()
    .then(() => {
      document.getElementById('prompt_form').submit(); 
    });

    const submitBtn = document.getElementById('generate-button');

submitBtn.addEventListener('click', () => {

  submitBtn.disabled = true;
  
  document.getElementById('loader-overlay').style.display = 'block';

  setTimeout(() => {
    submitBtn.disabled = false;
    document.getElementById('prompt_form').submit();
  }, 300);

});

// After form submit
document.getElementById('prompt_form').addEventListener('onload', () => {
    document.getElementById('loader-overlay').style.display = 'none'; 
  });