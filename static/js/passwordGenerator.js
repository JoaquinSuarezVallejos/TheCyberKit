// PASSWORD GENERATOR (JavaScript file)
/* Case types used: camelCase (for functions and variables), and kebab-case (for CSS classes) */

// Get references to password-related UI elements
// const passwordOutput = document.querySelector(
//   ".password-generator-readonly-box"
// );
const outputField = document.querySelector('.password-generator-readonly-box'); // Use a single variable for the output field
const generatePasswordBtn = document.querySelector(".generate-password-btn");
const copyToClipboardBtn = document.querySelector(".copy-to-clipboard-btn");
const typeRadios = document.querySelectorAll(
  'input[name="password-passphrase"]'
);
const charSlider = document.querySelector(".characters-slider");
const charCountDisplay = document.querySelector(".password-char-length");
const includeCheckboxes = document.querySelectorAll(
  '.password-generator-checkbox input[type="checkbox"]'
);

// Get all the important checkboxes by their IDs
const importantCheckboxes = document.querySelectorAll(
  "#uppercase-checkbox, #lowercase-checkbox, #numbers-checkbox, #symbols-checkbox"
);

// Get references to passphrase-related UI elements
// const passphraseOutput = document.querySelector(
//   ".password-generator-readonly-box"
// );
const wordsSlider = document.querySelector(".words-slider");
const wordsCountDisplay = document.querySelector(".passphrase-word-length");
const capitalizeCheckbox = document.getElementById("capitalize-checkbox");
const allCapsCheckbox = document.getElementById("all-caps-checkbox");
const addNumbersCheckbox = document.getElementById("add-numbers-checkbox");
const wordSeparatorInput = document.getElementById("word-separator-input-box");

// Get references to the elements that need to be hidden or shown based on the type (password/passphrase)
const charactersOptions = document.querySelector(".characters-option");
const wordsOptions = document.querySelector(".words-option");
const includeOptions = document.querySelector(".include-options");
const passphraseIncludeOptions = document.querySelector(
  ".passphrase-include-options"
);
const passphraseWordSeparator = document.querySelector(
  ".passphrase-word-separator"
);

/* UPDATE THE UI BASED ON THE SELECTED TYPE (PASSWORD/PASSPHRASE) */
/* -------------------------------------------------------------------------- */
function updateUIBasedOnType() {
  if (
    document.querySelector(
      'input[name="password-passphrase"][value="password"]'
    ).checked
  ) {
    charactersOptions.classList.remove("hidden");
    wordsOptions.classList.add("hidden");
    includeOptions.classList.remove("hidden");
    passphraseIncludeOptions.classList.add("hidden");
    passphraseWordSeparator.classList.add("hidden");
  } else {
    charactersOptions.classList.add("hidden");
    wordsOptions.classList.remove("hidden");
    includeOptions.classList.add("hidden");
    passphraseIncludeOptions.classList.remove("hidden");
    passphraseWordSeparator.classList.remove("hidden");
  }
}

// Add event listeners to the type radio buttons
typeRadios.forEach((radio) => {
  radio.addEventListener("change", () => {
    updateUIBasedOnType();
    if (radio.value === "password") {
      generatePassword();
    } else {
      generatePassphrase();
    }
  });
});

generatePasswordBtn.addEventListener("click", () => {
  if (
    document.querySelector(
      'input[name="password-passphrase"][value="password"]'
    ).checked
  ) {
    generatePassword();
  } else {
    generatePassphrase();
  }
});
/* -------------------------------------------------------------------------- */

/* ENABLE AND DISABLE "REGENERATE PASSWORD" BUTTON IF NO CHECKBOXES ARE CHECKED */
/* -------------------------------------------------------------------------- */
// Add a click event listener to each checkbox
importantCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("click", (event) => {
    // Count the number of checked checkboxes
    const checkedCount = Array.from(importantCheckboxes).filter(
      (cb) => cb.checked
    ).length;

    if (checkedCount === 0) {
      // If no checkboxes are checked, disable the generate button
      generatePasswordBtn.disabled = true;
    } else {
      // If at least one checkbox is checked, enable the generate button
      generatePasswordBtn.disabled = false;
    }
  });
});
/* -------------------------------------------------------------------------- */

/* GENERATE PASSWORD */
/* -------------------------------------------------------------------------- */
// Event listener to generate a password on page load and update the UI based on the type (password/passphrase)
document.addEventListener("DOMContentLoaded", () => {
  generatePassword();
  updateUIBasedOnType();
});
// Function to fetch a new password from the backend
function generatePassword() {
  // Gather parameters from the UI
  const type = document.querySelector(
    'input[name="password-passphrase"]:checked'
  ).value;
  const length = charSlider.value;
  const includeUppercase =
    document.getElementById("uppercase-checkbox").checked;
  const includeLowercase =
    document.getElementById("lowercase-checkbox").checked;
  const includeNumbers = document.getElementById("numbers-checkbox").checked;
  const includeSymbols = document.getElementById("symbols-checkbox").checked;

  // Send a POST request to the Flask backend
  fetch("/generate_password_or_passphrase", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type: type,
      length: length,
      use_uppercase: includeUppercase,
      use_lowercase: includeLowercase,
      use_numbers: includeNumbers,
      use_symbols: includeSymbols,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error("Error generating password/passphrase:", data.error); // Display an error message
      } else {
        // passwordOutput.value = data.generated_string;
        outputField.value = data.generated_string; // Update the single output field
      }
      // Check password length and apply the class if needed
      if (
        data.generated_string.length > 38 &&
        data.generated_string.length <= 45
      ) {
        removeSmallerFontClasses();
        outputField.classList.add("readonly-box-smaller-font1");
      } else if (
        data.generated_string.length > 45 &&
        data.generated_string.length <= 54
      ) {
        removeSmallerFontClasses();
        outputField.classList.add("readonly-box-smaller-font2");
      } else if (data.generated_string.length > 54) {
        removeSmallerFontClasses();
        outputField.classList.add("readonly-box-smaller-font3");
      } else {
        removeSmallerFontClasses();
      }
      function removeSmallerFontClasses() {
        outputField.classList.remove("readonly-box-smaller-font1");
        outputField.classList.remove("readonly-box-smaller-font2");
        outputField.classList.remove("readonly-box-smaller-font3");
      }
    })
    .catch((error) => {
      console.error("Error fetching password/passphrase:", error); // Display an error message
    });
}

// Add event listeners for password-related UI elements
// generatePasswordBtn.addEventListener("click", generatePassword);
charSlider.addEventListener("input", () => {
  charCountDisplay.textContent = `${charSlider.value}`;
  generatePassword(); // Regenerate password when slider value changes
});
// typeRadios.forEach((radio) => {
//   radio.addEventListener("change", generatePassword);
// });
includeCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", generatePassword);
});
/* -------------------------------------------------------------------------- */

/* GENERATE PASSPHRASE */
/* -------------------------------------------------------------------------- */
// Function to generate a passphrase
function generatePassphrase() {
  // Gather parameters from the UI
  const numWords = wordsSlider.value;
  const capitalizeFirst = capitalizeCheckbox.checked;
  const capitalizeAll = allCapsCheckbox.checked;
  const wordSeparator = String(wordSeparatorInput.value || '-'); // Default to "-" if empty
  const addNumbers = addNumbersCheckbox.checked;

  // Send a POST request to the Flask backend
  fetch("/generate_password_or_passphrase", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type: "passphrase",
      num_words: numWords,
      capitalize_first: capitalizeFirst,
      capitalize_all: capitalizeAll,
      word_separator: wordSeparator,
      add_numbers: addNumbers,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error("Error generating passphrase:", data.error);
        // Display an error message to the user
      } else {
        // passphraseOutput.value = data.generated_string; 
        outputField.value = data.generated_string; // Update the single output field
      }
    })
    .catch((error) => {
      console.error("Error fetching passphrase:", error);
      // Display an error message to the user
    });
}

// Add event listeners for passphrase-related UI elements

// generatePasswordBtn.addEventListener("click", () => {
//   if (
//     document.querySelector(
//       'input[name="password-passphrase"][value="password"]'
//     ).checked
//   ) {
//     generatePassword();
//   } else {
//     generatePassphrase();
//   }
// });

wordsSlider.addEventListener("input", () => {
  wordsCountDisplay.textContent = `${wordsSlider.value}`;
  generatePassphrase();
});

capitalizeCheckbox.addEventListener("change", generatePassphrase);
allCapsCheckbox.addEventListener("change", generatePassphrase);
addNumbersCheckbox.addEventListener("change", generatePassphrase);
// wordSeparatorInput.addEventListener("input", generatePassphrase);

wordSeparatorInput.addEventListener("input", () => {
  console.log("Current word separator:", wordSeparatorInput.value); // Debug print
  generatePassphrase();
});
/* -------------------------------------------------------------------------- */

/* COPY TO CLIPBOARD */
/* -------------------------------------------------------------------------- */
copyToClipboardBtn.addEventListener("click", () => {
  const passwordToCopy = outputField.value;

  navigator.clipboard
    .writeText(passwordToCopy) // Copy the password to the clipboard
    .then(() => {
      console.log("Password copied to clipboard!");

      // Store the original button text and color (excluding the font-awesome icon)
      const originalText = copyToClipboardBtn.childNodes[2].nodeValue.trim();
      const originalColor = copyToClipboardBtn.style.backgroundColor;

      // Change the button text and color
      copyToClipboardBtn.childNodes[2].nodeValue = " Copied!";
      copyToClipboardBtn.style.backgroundColor = "#DAD4C2"; // Pico CSS color used: Sand 150 (Stonewashed)

      // Prevent further clicks for 1 second
      copyToClipboardBtn.addEventListener(
        "click",
        preventDefaultForOneSecond,
        true
      );

      // Change the text and color back after 1 second
      setTimeout(() => {
        copyToClipboardBtn.childNodes[2].nodeValue = " " + originalText;
        copyToClipboardBtn.style.backgroundColor = originalColor;
        copyToClipboardBtn.removeEventListener(
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

// TODO: Implement the password tester functionality
// TODO: Implement the passphrase generator functionality
// TODO: Make an "expanding animation" for the password-generator-readonly-box when a new password is generated
