document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function() {
      document.querySelector('.card').style.opacity = '0.6';
      var submitButton = document.querySelector('button[type="submit"]');
      submitButton.innerHTML = 'Analyzing...';
      submitButton.disabled = true;
    });
  });
  