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
    .then(response => response.json())
    .then(data => {
      scoreResult.textContent = data.score;
        timeToCrack.textContent = data.crack_time;
    });
});

passwordTesterInput.addEventListener('keydown', (event) => {
  if (event.key === ' ') { // Check if the pressed key is a space
      event.preventDefault(); // Prevent the default action (entering the space)
  }
});