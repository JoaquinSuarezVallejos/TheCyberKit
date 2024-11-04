// ENCRYPTOR / DECRYPTOR (JavaScript file)

// Get elements
const encryptRadioBtn = document.getElementById("encryption-radio-btn");
const decryptRadioBtn = document.getElementById("decryption-radio-btn");
const encryptDecryptSubmitBtn = document.querySelector(
  ".encrypt-decrypt-submit-btn"
);
const inputLabel = document.querySelector(".encryption-decryption-input-label");
const inputLabel2 = document.querySelector(".encryption-decryption-input-label2")
const outputLabel = document.querySelector(
  ".encryption-decryption-output-label"
);

// Listen for radio button changes
encryptRadioBtn.addEventListener("change", updateAction);
decryptRadioBtn.addEventListener("change", updateAction);

// Update action button, labels, and placeholder based on selected radio button
function updateAction() {
  if (encryptRadioBtn.checked) {
    encryptDecryptSubmitBtn.textContent = "Encrypt";
    inputLabel.textContent = "Enter text to encrypt:";
    inputLabel2.textContent = "Encrypt with a custom secret key:"
    outputLabel.textContent = "Encrypted text output:";
  } else if (decryptRadioBtn.checked) {
    encryptDecryptSubmitBtn.textContent = "Decrypt";
    inputLabel.textContent = "Enter text to decrypt:";
    inputLabel2.textContent = "Decryption requires a custom secret key:"
    outputLabel.textContent = "Decrypted text output:";
  } else {
    // Default to encrypt
    encryptDecryptSubmitBtn.textContent = "Encrypt";
    inputLabel.textContent = "Enter text to encrypt:";
    inputLabel2.textContent = "Encrypt with a custom secret key:"
    outputLabel.textContent = "Encrypted text output:";
  }
}
