// Function to update the price
function updatePrice() {
  fetch('/api/price')
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Add highlight effect to the card
        const priceCard = document.getElementsByClassName('price-card')[0];
        if (priceCard) {
          priceCard.classList.remove('highlight');
          // Trigger reflow to restart animation
          void priceCard.offsetWidth;
          priceCard.classList.add('highlight');
        }

        // Update the price
        document.getElementById('price').textContent = `$${data.price.toLocaleString()}`;

        // Update the change percentage
        const changeElement = document.getElementById('change');
        changeElement.textContent = `${data.change_24h > 0 ? '+' : ''}${data.change_24h}%`;
        changeElement.className = `change ${data.change_24h >= 0 ? 'positive' : 'negative'}`;

        // Update min and max values (converting k to thousand)
        const minValue = data.min >= 1000 ? '$' + (data.min / 1000).toFixed(3) : data.min;
        const maxValue = data.max >= 1000 ? '$' + (data.max / 1000).toFixed(3) : data.max;

        document.getElementById('min-price').textContent = minValue;
        document.getElementById('max-price').textContent = maxValue;

        // Update progress bar (relative position of current price)
        const progress = ((data.price - data.min) / (data.max - data.min)) * 100;
        document.getElementById('range-progress').style.width = `${Math.max(5, Math.min(95, progress))}%`;

        // Hide error messages
        document.getElementById('error').style.display = 'none';

        // Update last update time
        const now = new Date();
        document.getElementById('last-update').textContent =
          `Last update: ${now.toLocaleTimeString('pt-BR')}`;
      } else {
        showError(data.error || 'Error retrieving data');
      }
    })
    .catch(error => {
      showError('Connection error: ' + error.message);
    });
}

// Function to display errors
function showError(message) {
  const errorElement = document.getElementById('error');
  errorElement.textContent = message;
  errorElement.style.display = 'block';
}

// Initial configuration when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Update price initially
  updatePrice();

  // Update automatically every 3 seconds
  setInterval(updatePrice, 3000);
});
