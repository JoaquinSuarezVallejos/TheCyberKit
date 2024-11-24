// ENCRYPTOR/DECRYPTOR (JavaScript file)

// Get elements
const encryptRadioBtn = document.getElementById("encryption-radio-btn");
const decryptRadioBtn = document.getElementById("decryption-radio-btn");
const encryptDecryptSubmitBtn = document.querySelector(
  ".encrypt-decrypt-submit-btn"
);
const inputLabel = document.querySelector(".encryption-decryption-input-label");
const inputLabel2 = document.querySelector(
  ".encryption-decryption-input-label2"
);
const outputLabel = document.querySelector(
  ".encryption-decryption-output-label"
);
const encryptionDecryptionTextAreaInput = document.getElementById(
  "encryption-decryption-textarea-input"
);
const customKeyInputBox = document.querySelector(".custom-key-input-box");
const encryptionDecryptionTextAreaOutput = document.getElementById(
  "encryption-decryption-textarea-output"
);
const encryptionMethodSelect = document.getElementById(
  "encryption-method-select"
);

// Listen for radio button changes
encryptRadioBtn.addEventListener("change", updateFields);
decryptRadioBtn.addEventListener("change", updateFields);

function resetTextFields() {
  encryptionDecryptionTextAreaInput.value = "";
  encryptionDecryptionTextAreaOutput.value = "";
  customKeyInputBox.value = "";
}

// Reset text fields and update fields for encryption
function updateFieldsForEncryption() {
  encryptDecryptSubmitBtn.textContent = "Encrypt";
  inputLabel.textContent = "Enter text to encrypt:";
  inputLabel2.textContent = "Encrypt with a custom secret key:";
  outputLabel.textContent = "Encrypted text output:";

  const placeholderOption =
    encryptionMethodSelect.querySelector("option[disabled]");
  placeholderOption.textContent = "Select an encryption method";

  resetTextFields();
}

// Reset text fields and update fields for decryption
function updateFieldsForDecryption() {
  encryptDecryptSubmitBtn.textContent = "Decrypt";
  inputLabel.textContent = "Enter text to decrypt:";
  inputLabel2.textContent = "Decryption requires a custom secret key:";
  outputLabel.textContent = "Decrypted text output:";

  const placeholderOption =
    encryptionMethodSelect.querySelector("option[disabled]");
  placeholderOption.textContent = "Select a decryption method";

  resetTextFields();
}

// Update encrypt/decrypt button, labels, and placeholders based on the selected radio button ("Encryption" or "Decryption")
function updateFields() {
  if (encryptRadioBtn.checked) {
    // Update fields for encryption
    updateFieldsForEncryption();
  } else if (decryptRadioBtn.checked) {
    // Update fields for decryption
    updateFieldsForDecryption();
  } else {
    // Default to encryption
    updateFieldsForEncryption();
  }
}

// Update the event listener for the Encrypt/Decrypt button
encryptDecryptSubmitBtn.addEventListener("click", async () => {
  const text = encryptionDecryptionTextAreaInput.value.trim();
  const key = customKeyInputBox.value.trim();
  const method = document.querySelector(
    'input[name="encryption-method"]:checked'
  ).value; // e.g., "Fernet", "Blowfish", or "AES"

  if (!text || !key || !method) {
    encryptionDecryptionTextAreaOutput.value =
      "Please provide all inputs (text, key, method).";
    return;
  }

  const url = encryptRadioBtn.checked ? "/encrypt" : "/decrypt";
  const action = encryptRadioBtn.checked ? "encrypt" : "decrypt";

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, key, method }),
    });

    const result = await response.json();

    if (response.ok) {
      encryptionDecryptionTextAreaOutput.value = result[`${action}ed_text`]; // Use "encrypted_text" or "decrypted_text"
    } else {
      encryptionDecryptionTextAreaOutput.value = `Error: ${result.error}`;
    }
  } catch (error) {
    encryptionDecryptionTextAreaOutput.value = `Request failed: ${error.message}`;
  }
});
