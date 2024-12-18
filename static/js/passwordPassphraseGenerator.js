// PASSWORD/PASSPHRASE GENERATOR (JavaScript file)

// Get references to password-related UI elements
const outputField = document.querySelector(".password-generator-readonly-box"); // Single variable for the output field
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

/* ENABLE/DISABLE "REGENERATE PASSWORD" BUTTON */
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
// On page load
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
        console.error("Error generating password: ", data.error);
        // Display an error message
        outputField.innerHTML = "---";
      } else {
        // Apply color formatting to the password
        const formattedPassword = updatePasswordColors(
          data.generated_string,
          includeNumbers,
          includeSymbols
        );
        outputField.innerHTML = formattedPassword; // Update using innerHTML
        evaluatePasswordStrength(data.generated_string); // Call the evaluation function with the generated password

        expandAnimationOutputField(); // Trigger the expand animation
      }
    })
    .catch((error) => {
      console.error("Error fetching password: ", error); // Display an error message
      outputField.innerHTML = "---";
    });
}

// Add event listeners for password-related UI elements
charSlider.addEventListener("input", () => {
  charCountDisplay.textContent = `${charSlider.value}`;
  generatePassword(); // Regenerate password when slider value changes
});
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
  const addNumbers = addNumbersCheckbox.checked;
  const wordSeparator = String(wordSeparatorInput.value || "-"); // Default to "-" if empty

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
      add_numbers: addNumbers,
      word_separator: wordSeparator,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error("Error generating passphrase: ", data.error);
        // Display an error message to the user
        outputField.innerHTML = "---";
      } else {
        // Apply colors to the passphrase
        const formattedPassphrase = updatePassphraseColors(
          data.generated_string,
          wordSeparator
        );
        outputField.innerHTML = formattedPassphrase;
        evaluatePasswordStrength(data.generated_string); // Call the evaluation function with the generated passphrase

        expandAnimationOutputField(); // Trigger the expand animation
      }
    })
    .catch((error) => {
      console.error("Error fetching passphrase: ", error);
      // Display an error message to the user
      outputField.innerHTML = "---";
    });
}

wordsSlider.addEventListener("input", () => {
  wordsCountDisplay.textContent = `${wordsSlider.value}`;
  generatePassphrase();
});

capitalizeCheckbox.addEventListener("change", generatePassphrase);
allCapsCheckbox.addEventListener("change", generatePassphrase);
addNumbersCheckbox.addEventListener("change", generatePassphrase);

wordSeparatorInput.addEventListener("input", () => {
  console.log("Current word separator:", wordSeparatorInput.value); // Debug print
  generatePassphrase();
});
/* -------------------------------------------------------------------------- */

/* COPY TO CLIPBOARD */
/* -------------------------------------------------------------------------- */
copyToClipboardBtn.addEventListener("click", () => {
  const passwordToCopy = outputField.textContent;

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

/* EVALUATE PASSWORD/PASSPHRASE STRENGTH (PASSWORD TESTER) */
/* -------------------------------------------------------------------------- */
function evaluatePasswordStrength(password) {
  // Get the selected scenario (online or offline)
  const scenario = document.querySelector(
    'input[name="scenario-online-offline"]:checked'
  ).value;

  fetch("/evaluate_password_generator", {
    // Send a POST request to the Flask backend
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ password: password, scenario: scenario }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Get the elements by their IDs
      const scoreResult = document.getElementById(
        "password-generator-score-result"
      );
      const timeToCrack = document.getElementById(
        "password-generator-crack-time"
      );

      // Set the text content for score and crack time
      scoreResult.textContent = `${data.score}`;
      timeToCrack.textContent = `${data.crack_time}`;

      // Remove any existing score classes from both elements
      for (let i = 1; i <= 5; i++) {
        // Adjusted to loop from 1 to 5 based on score range
        scoreResult.classList.remove(`score-${i}`);
        timeToCrack.classList.remove(`score-${i}`);
      }

      // Extract the numeric score
      const match = data.score.match(/^\d+/);
      const numericScore = match ? parseInt(match[0]) : -1;

      // Add the appropriate score class to both elements
      if (numericScore >= 1 && numericScore <= 5) {
        // Adjusted to reflect score range 1-5
        scoreResult.classList.add(`score-${numericScore}`);
        timeToCrack.classList.add(`score-${numericScore}`);
      } else {
        console.error("Invalid score received from backend:", data.score);
      }
    })
    .catch((error) => {
      console.error("Error evaluating password strength:", error);
    });
}

/* UPDATE PASSWORD/PASSPHRASE STRENGTH WHEN CLICKING ANY OF THE RADIO BTNS (ONLINE OR OFFLINE) */
const scenarioRadioButtons = document.querySelectorAll(
  'input[name="scenario-online-offline"]'
); // Get references to the radio buttons

// Attach an event listener to each radio button
scenarioRadioButtons.forEach((radioButton) => {
  radioButton.addEventListener("change", () => {
    // Get the current password displayed in the password generator
    const currentPassword = document.querySelector(
      ".password-generator-readonly-box"
    ).textContent;

    // Call the evaluatePasswordStrength function with the current password
    evaluatePasswordStrength(currentPassword);
  });
});
/* -------------------------------------------------------------------------- */

/* PASSWORD COLORING */
/* -------------------------------------------------------------------------- */
function updatePasswordColors(password, includeNumbers, includeSymbols) {
  let formattedPassword = "";

  // Loop through each character in the password
  for (let char of password) {
    if (/\d/.test(char) && includeNumbers) {
      // Check if it's a number and "includeNumbers" is true
      formattedPassword += `<span class="blue-numbers">${char}</span>`;
    } else if (/[^a-zA-Z0-9]/.test(char) && includeSymbols) {
      // Check if it's a symbol and "includeSymbols" is true
      formattedPassword += `<span class="orange-symbols">${char}</span>`;
    } else {
      // Leave it unchanged for letters
      formattedPassword += char;
    }
  }
  return formattedPassword;
}
/* -------------------------------------------------------------------------- */

/* PASSPHRASE COLORING */
/* -------------------------------------------------------------------------- */
function updatePassphraseColors(passphrase, separator) {
  let formattedPassphrase = "";

  // Split the passphrase into words based on the separator
  const words = passphrase.split(separator);

  words.forEach((word, index) => {
    let formattedWord = "";

    // Loop through each character in the word
    for (let char of word) {
      if (/\d/.test(char)) {
        // Color numbers in blue
        formattedWord += `<span class="blue-numbers">${char}</span>`;
      } else if (/[^a-zA-Z0-9]/.test(char)) {
        // Color symbols in orange
        formattedWord += `<span class="orange-symbols">${char}</span>`;
      } else {
        // Leave letters unchanged
        formattedWord += char;
      }
    }

    // Append the formatted word
    formattedPassphrase += formattedWord;

    // Add the separator with the appropriate styling
    if (index < words.length - 1) {
      if (/^[a-zA-Z]$/.test(separator)) {
        // If separator is a letter, style it in grey
        formattedPassphrase += `<span class="grey-letters">${separator}</span>`;
      } else if (/\d/.test(separator)) {
        formattedPassphrase += `<span class="blue-numbers">${separator}</span>`;
      } else {
        // If separator is not a letter, style it in orange
        formattedPassphrase += `<span class="orange-symbols">${separator}</span>`;
      }
    }
  });

  return formattedPassphrase;
}
/* -------------------------------------------------------------------------- */

/* EXPAND ANIMATION WHEN A PASSWORD/PASSPHRASE IS GENERATED */
/* -------------------------------------------------------------------------- */
function expandAnimationOutputField() {
  outputField.classList.remove("expand");
  void outputField.offsetWidth; // Trigger reflow to restart the animation
  outputField.classList.add("expand");
}
/* -------------------------------------------------------------------------- */
