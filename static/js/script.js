// JS File

const dynamicText = document.getElementById('dynamic-text');
const originalText = dynamicText.textContent;
const modifiedText = "Th3Cyb3rK1t";

setInterval(() => {
  if (dynamicText.textContent === originalText) {
    dynamicText.textContent = modifiedText;
    dynamicText.classList.add('glitch'); // Add glitch class
    setTimeout(() => {
      dynamicText.classList.remove('glitch'); // Remove glitch class after a short delay
    }, 1000); // Adjust delay as needed
  } else {
    dynamicText.textContent = originalText;
  }
}, 5000);