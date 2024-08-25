// Vanilla JavaScript File

const cyberkitTitleText = document.getElementById('cyberkit_title_text');
const originalText = cyberkitTitleText.textContent;

function transitionToModifiedText() {
  // First 'e' to '3'
  setTimeout(() => {
    cyberkitTitleText.textContent = originalText.replace('e', '3');
    addGlowEffect();
  }, 0); // No delay for the first change

  // Second 'e' to '3'
  setTimeout(() => {
    cyberkitTitleText.textContent = cyberkitTitleText.textContent.replace('e', '3');
    addGlowEffect();
  }, 1000); // 1-second delay

  // 'i' to '1'
  setTimeout(() => {
    cyberkitTitleText.textContent = cyberkitTitleText.textContent.replace('i', '1');
    cyberkitTitleText.classList.add('modified');
  }, 2000); // 2-second delay

  // Change back to original after a delay
  setTimeout(() => {
    cyberkitTitleText.classList.remove('modified');
    cyberkitTitleText.textContent = originalText;
  }, 4000); // 4-second delay (2s for modified + 2s delay)
}

function addGlowEffect() {
  const modifiedText = cyberkitTitleText.textContent;
  cyberkitTitleText.innerHTML = ''; // Clear the current text content

  for (let char of modifiedText) {
    const span = document.createElement('span');
    span.textContent = char;
    if (char === '3') {
      span.classList.add('glow');
    }
    cyberkitTitleText.appendChild(span);
  }
}

setInterval(transitionToModifiedText, 10000); // Total cycle time: 8s (original) + 2s (transition) = 10s