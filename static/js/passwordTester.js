// PASSWORD TESTER (JavaScript file)
/* Case types used: camelCase (for functions and variables), 
SCREAMING_SNAKE_CASE (for constants) and kebab-case (for CSS classes) */

const passwordTesterInput = document.querySelector('.password-tester-input-box');
const scoreResult = document.getElementById('password-score-result');
const timeToCrack = document.getElementById('password-crack-time');

// Get references to the radio buttons
const onlineRadioBtn = document.getElementById('online-radio-btn');
const offlineRadioBtn = document.getElementById('offline-radio-btn');

// Function to update the displayed crack time
function updateCrackTimeDisplay(data) {
  if (onlineRadioBtn.checked) {
    timeToCrack.textContent = data.crack_time_online_throttled;
  } else if (offlineRadioBtn.checked) {
    timeToCrack.textContent = data.crack_time_offline;
  }
}

passwordTesterInput.addEventListener('input', () => {
    const password = passwordTesterInput.value;

    fetch('/evaluate_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => {
        if (!response.ok) { 
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Received data from backend:", data); 

        scoreResult.textContent = data.score;
        updateCrackTimeDisplay(data); // Update crack time based on selected radio button

        // Remove any existing score classes from both elements
        for (let i = 0; i <= 5; i++) {
            scoreResult.classList.remove(`score-${i}`);
            timeToCrack.classList.remove(`score-${i}`); 
        }

        // Extract the numeric score
        const match = data.score.match(/^\d+/);
        const numericScore = match ? parseInt(match[0]) : -1;

        // Add the appropriate score class to both elements
        if (numericScore >= 0 && numericScore <= 5) {
            scoreResult.classList.add(`score-${numericScore}`);
            timeToCrack.classList.add(`score-${numericScore}`); 
        } else {
            console.error("Invalid score received from backend:", data.score); 
        }
    })
    .catch(error => {
        console.error('Error fetching password evaluation:', error);
        scoreResult.textContent = 'Error evaluating password';
        timeToCrack.textContent = '';
    });
});

// Function to fetch the crack time and update the display
function fetchAndUpdateCrackTime() {
  fetch('/evaluate_password', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ password: passwordTesterInput.value }) 
  })
  .then(response => response.json())
  .then(data => {
      updateCrackTimeDisplay(data);
  });
}

// Add event listeners to the radio buttons
onlineRadioBtn.addEventListener('change', fetchAndUpdateCrackTime);
offlineRadioBtn.addEventListener('change', fetchAndUpdateCrackTime);

passwordTesterInput.addEventListener('keydown', (event) => {
    if (event.key === ' ') { 
        event.preventDefault(); 
    }
});

// Initial update when the page loads (assuming 'online' is checked by default)
passwordTesterInput.dispatchEvent(new Event('input'));