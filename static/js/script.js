/* Case types used: camelCase (for functions and variables), 
SCREAMING_SNAKE_CASE (for constants) and kebab-case (for CSS classes) */

// CyberKit Title Section
const CYBERKIT_TITLE_TEXT = document.getElementById('cyberkit-title-text');
const ORIGINAL_TEXT = CYBERKIT_TITLE_TEXT.textContent;

function transitionToModifiedText() {
  // First 'e' to '3'
  setTimeout(() => {
    CYBERKIT_TITLE_TEXT.textContent = ORIGINAL_TEXT.replace('e', '3');
    addGlowEffect();
  }, 0); // No delay for the first change

  // Second 'e' to '3'
  setTimeout(() => {
    CYBERKIT_TITLE_TEXT.textContent = CYBERKIT_TITLE_TEXT.textContent.replace('e', '3');
    addGlowEffect();
  }, 1000); // 1-second delay

  // 'i' to '1'
  setTimeout(() => {
    CYBERKIT_TITLE_TEXT.textContent = CYBERKIT_TITLE_TEXT.textContent.replace('i', '1');
    CYBERKIT_TITLE_TEXT.classList.add('modified');
  }, 2000); // 2-second delay

  // Change back to original after a delay
  setTimeout(() => {
    CYBERKIT_TITLE_TEXT.classList.remove('modified');
    CYBERKIT_TITLE_TEXT.textContent = ORIGINAL_TEXT;
  }, 4000); // 4-second delay (2s for modified + 2s delay)
}

function addGlowEffect() {
  const MODIFIED_TEXT = CYBERKIT_TITLE_TEXT.textContent;
  CYBERKIT_TITLE_TEXT.innerHTML = ''; // Clear the current text content

  for (let char of MODIFIED_TEXT) {
    const span = document.createElement('span');
    span.textContent = char;
    if (char === '3') {
      span.classList.add('glow');
    }
    CYBERKIT_TITLE_TEXT.appendChild(span);
  }
}

// Total cycle time: 8s (showing original text) + 4s (transition + showing modified text) = 12s
setInterval(transitionToModifiedText, 12000); 


// Password Tester Section
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