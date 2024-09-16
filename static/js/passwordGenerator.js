// PASSWORD GENERATOR (JavaScript file)

/* Case types used: camelCase (for functions and variables), 
SCREAMING_SNAKE_CASE (for constants) and kebab-case (for CSS classes) */

/* Enable and Disable generate-password-btn */
/* -------------------------------------------------------------------------- */

// Get all the desired checkboxes by their IDs
const checkboxes = document.querySelectorAll(
  '#uppercase-checkbox, #lowercase-checkbox, #numbers-checkbox, #symbols-checkbox'
);
const generatePasswordBtn = document.querySelector(".generate-password-btn");

// Add a click event listener to each checkbox
checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("click", (event) => {
    // Count the number of checked checkboxes
    const checkedCount = Array.from(checkboxes).filter(
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

