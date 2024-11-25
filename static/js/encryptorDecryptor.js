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

// COPY TO CLIPBOARD FOR ENCRYPTED TEXT OUTPUT
/* -------------------------------------------------------------------------- */
const copyToClipboardBtn2 = document.querySelector(".copy-to-clipboard-btn2");

copyToClipboardBtn2.addEventListener("click", () => {
  let encryptedTextToCopy = encryptionDecryptionTextAreaOutput.value.trim(); // Get the encrypted text from the output textarea

  // If the text is empty, copy the placeholder "[.....]" instead
  if (!encryptedTextToCopy) {
    encryptedTextToCopy = "[.....]";
  }

  navigator.clipboard
    .writeText(encryptedTextToCopy) // Copy the text to the clipboard (either the actual content or "[.....]")
    .then(() => {
      console.log("Encrypted/decrypted text copied to clipboard!");

      // Store the original button text and color (excluding the font-awesome icon)
      const originalText = copyToClipboardBtn2.childNodes[2].nodeValue.trim();
      const originalColor = copyToClipboardBtn2.style.backgroundColor;

      // Change the button text and color
      copyToClipboardBtn2.childNodes[2].nodeValue = " Copied!";
      copyToClipboardBtn2.style.backgroundColor = "#DAD4C2"; // Pico CSS color used: Sand 150 (Stonewashed)

      // Prevent further clicks for 1 second
      copyToClipboardBtn2.addEventListener(
        "click",
        preventDefaultForOneSecond,
        true
      );

      // Change the text and color back after 1 second
      setTimeout(() => {
        copyToClipboardBtn2.childNodes[2].nodeValue = " " + originalText;
        copyToClipboardBtn2.style.backgroundColor = originalColor;
        copyToClipboardBtn2.removeEventListener(
          "click",
          preventDefaultForOneSecond,
          true
        );
      }, 1000);
    })
    .catch((err) => {
      console.error("Could not copy text: ", err);
    });
});

function preventDefaultForOneSecond(event) {
  event.preventDefault(); // Prevent the default click behavior
  event.stopImmediatePropagation(); // Stop the event from bubbling up
}
/* -------------------------------------------------------------------------- */
