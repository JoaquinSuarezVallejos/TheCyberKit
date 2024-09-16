// PASSWORD GENERATOR (JavaScript file)
/* Case types used: camelCase (for functions and variables), 
SCREAMING_SNAKE_CASE (for constants) and kebab-case (for CSS classes) */

// Get references to UI elements
const passwordOutput = document.querySelector(
  ".password-generator-readonly-box"
);
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

/* ENABLE AND DISABLE "REGENERATE PASSWORD" BUTTON */
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

/* PASSWORD GENERATOR FUNCTIONALITY */
/* -------------------------------------------------------------------------- */
// Function to fetch a new password/passphrase from the backend
function generatePasswordOrPassphrase() {
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
  const noRepeats = document.getElementById("no-repeats-checkbox").checked;

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
      no_repeats: noRepeats,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error("Error generating password/passphrase:", data.error); // Display an error message
      } else {
        passwordOutput.value = data.generated_string;
      }
    })
    .catch((error) => {
      console.error("Error fetching password/passphrase:", error); // Display an error message
    });
}

// Add event listeners
generatePasswordBtn.addEventListener("click", generatePasswordOrPassphrase);
charSlider.addEventListener("input", () => {
  charCountDisplay.textContent = `Characters: ${charSlider.value}`;
});
typeRadios.forEach((radio) => {
  radio.addEventListener("change", generatePasswordOrPassphrase);
});
includeCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", generatePasswordOrPassphrase);
});

// Copy password to clipboard functionality
copyToClipboardBtn.addEventListener("click", () => {
  const passwordToCopy = passwordOutput.value;

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
        copyToClipboardBtn.removeEventListener('click', preventDefaultForOneSecond, true);
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
