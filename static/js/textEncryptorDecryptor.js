// ENCRYPTOR / DECRYPTOR (JavaScript file)

// Get elements
const encryptRadioBtn = document.getElementById('encryption-radio-btn');
const decryptRadioBtn = document.getElementById('decryption-radio-btn');
const encryptDecryptSubmitBtn = document.querySelector('.encrypt-decrypt-submit-btn');
const textInput = document.getElementById('text-input');
const outputText = document.getElementById('output-text');
const inputLabel = document.getElementById('input-label');
const outputLabel = document.getElementById('output-label');

// Listen for radio button changes
encryptRadioBtn.addEventListener('change', updateAction);
decryptRadioBtn.addEventListener('change', updateAction);

// Update action button, labels, and placeholder based on selected radio button
function updateAction() {
  if (encryptRadioBtn.checked) {
    actionBtn.textContent = 'Encrypt';
    inputLabel.textContent = 'Enter text to encrypt:';
    outputLabel.textContent = 'Encrypted text output:';
    textInput.placeholder = '[Enter text to encrypt...]';
    outputText.placeholder = '[Encrypted output...]';
  } else if (decryptRadioBtn.checked) {
    actionBtn.textContent = 'Decrypt';
    inputLabel.textContent = 'Enter text to decrypt:';
    outputLabel.textContent = 'Decrypted text output:';
    textInput.placeholder = '[Enter encrypted text...]';
    outputText.placeholder = '[Decrypted output...]';
  }
}

// Listen for button click
actionBtn.addEventListener('click', () => {
  const text = textInput.value;

  if (encryptRadioBtn.checked) {
    // Encrypt the text
    outputText.value = btoa(text);
  } else if (decryptRadioBtn.checked) {
    try {
      // Decrypt the text
      outputText.value = atob(text);
    } catch (e) {
      outputText.value = 'Invalid decryption input!';
    }
  }
});
