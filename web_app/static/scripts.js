
/**
 * Changes the tables that are currently selected.
 */
function selectCardsByTable(selectionTable) {
  // Do we have any selected dino cards?
  var allDinoCardsSelected = true;
  var atLeastOneNonDinoCardSelected = false;
  document.querySelectorAll('input[name="tables"]').forEach(checkbox => {
    if (selectionTable.includes(checkbox.value) && !checkbox.checked) {
      allDinoCardsSelected = false;
    }
    if (!(selectionTable.includes(checkbox.value)) && checkbox.checked) {
      atLeastOneNonDinoCardSelected = true;
    }
  });

  // If we have anything except exclusively all the dino cards selected,
  // turns the dino cards on.
  var checkboxValue;
  if (allDinoCardsSelected && !atLeastOneNonDinoCardSelected) {
    checkboxValue = false;
  } else {
    checkboxValue = true;
  }
  document.querySelectorAll('input[name="tables"]').forEach(checkbox => {
    if (selectionTable.includes(checkbox.value)) {
      checkbox.checked = checkboxValue;
    } else {
      checkbox.checked = false;
    }
  });

  document.querySelector('form').submit();
}

/**
 * Scroll to top button functionality.
 */
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}