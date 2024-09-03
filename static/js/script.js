// JAVASCRIPT FILE
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
      if (!response.ok) { // Check if the response is successful
        throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      console.log("Received data from backend:", data); 

      scoreResult.textContent = data.score;
      timeToCrack.textContent = data.crack_time;

      // Remove any existing score classes
      for (let i = 0; i <= 5; i++) { // Include 5 in the loop 
        scoreResult.classList.remove(`score-${i}`);
        timeToCrack.classList.remove(`score-${i}`);
      }

      // Extract numeric score, handling potential variations in the format
      const numericScoreMatch = data.score.match(/\d+/); // Match any sequence of digits
      const numericScore = numericScoreMatch ? parseInt(numericScoreMatch[0]) : -1;

      // Add the appropriate score class, only if the score is valid
      if (numericScore >= 0 && numericScore <= 5) { // Include 5 in the range
        scoreResult.classList.add(`score-${numericScore}`);
        timeToCrack.classList.add(`score-${numericScore}`); 
      } else {
          console.error("Invalid score received from backend:", data.score); // Log an error if the score is unexpected
      }
  })
  .catch(error => {
      console.error('Error fetching password evaluation:', error);
      // Optionally, display an error message to the user
      scoreResult.textContent = 'Error evaluating password';
      timeToCrack.textContent = '';
  });
});

passwordTesterInput.addEventListener('keydown', (event) => {
  if (event.key === ' ') { 
      event.preventDefault(); 
  }
});