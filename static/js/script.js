// JAVASCRIPT FILE
/* Case types used: camelCase (for functions and variables), 
SCREAMING_SNAKE_CASE (for constants) and kebab-case (for CSS classes) */

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