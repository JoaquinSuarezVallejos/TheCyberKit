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

// Event listener for the textarea input and the custom key input
encryptionDecryptionTextAreaInput.addEventListener("input", () => {
  encryptionDecryptionTextAreaOutput.value = "";
});
customKeyInputBox.addEventListener("input", () => {
  encryptionDecryptionTextAreaOutput.value = "";
});

// Event listener for the select combobox
encryptionMethodSelect.addEventListener("change", () => {
  encryptionDecryptionTextAreaOutput.value = "";
});

// Reset text fields and select dropdown
function resetTextFields() {
  encryptionDecryptionTextAreaInput.value = "";
  encryptionDecryptionTextAreaOutput.value = "";
  customKeyInputBox.value = "";
  encryptionMethodSelect.value = "";
}

// Update fields for encryption
function updateFieldsForEncryption() {
  encryptDecryptSubmitBtn.textContent = "Encrypt";
  inputLabel.textContent = "Enter text to encrypt:";
  inputLabel2.textContent = "Encrypt with a custom secret key:";
  outputLabel.textContent = "Encrypted text output:";
  resetTextFields();
}

// Update fields for decryption
function updateFieldsForDecryption() {
  encryptDecryptSubmitBtn.textContent = "Decrypt";
  inputLabel.textContent = "Enter text to decrypt:";
  inputLabel2.textContent = "Decryption requires a custom secret key:";
  outputLabel.textContent = "Decrypted text output:";
  resetTextFields();
}

// Update fields dynamically based on the selected radio button ("Encryption" or "Decryption")
function updateFields() {
  if (encryptRadioBtn.checked) {
    updateFieldsForEncryption();
  } else if (decryptRadioBtn.checked) {
    updateFieldsForDecryption();
  } else {
    updateFieldsForEncryption();
  }
}

// Handle encrypt/decrypt button click
encryptDecryptSubmitBtn.addEventListener("click", async () => {
  const text = encryptionDecryptionTextAreaInput.value.trim();
  const key = customKeyInputBox.value.trim();
  const method = encryptionMethodSelect.value; // Get selected method

  if (!text || !key || !method) {
    encryptionDecryptionTextAreaOutput.value =
      "> All fields are required: please provide the text, a custom key, and select an encryption/decryption method before proceeding.";
    return;
  }

  const url = encryptRadioBtn.checked ? "/encrypt" : "/decrypt";
  const action = encryptRadioBtn.checked ? "encrypted_text" : "decrypted_text";

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
      encryptionDecryptionTextAreaOutput.value = result[action];
    } else {
      encryptionDecryptionTextAreaOutput.value =
        result.error || "> An unknown error occurred.";
    }
  } catch (error) {
    encryptionDecryptionTextAreaOutput.value = `> Failed to connect to the server. Please try again.`;
  }
});

// Initialize fields based on default radio button (Encryption)
updateFields();
