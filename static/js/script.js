// Vanilla JavaScript File

const cyberkit_title_text = document.getElementById('cyberkit_title_text');
const originalText = cyberkit_title_text.textContent;
const modifiedText = "Th3Cyb3rK1t";

setInterval(() => {
  if (cyberkit_title_text.textContent === originalText) {
    cyberkit_title_text.textContent = modifiedText;
    cyberkit_title_text.classList.add('glitch'); // Add glitch class
    setTimeout(() => {
      cyberkit_title_text.classList.remove('glitch'); // Remove glitch class after a short delay
    }, 1000); // Adjust delay as needed
  } else {
    cyberkit_title_text.textContent = originalText;
  }
}, 5000);