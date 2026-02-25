/**
 * Scroll to top button functionality.
 */
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Selects a subset of all tables, and then renders cards corresponding to that table.
 * @param {list} subsetTable - all tables we will enable/disable
 */
function selectSubsetOfCards(subsetTable) {
  const checkboxes = document.querySelectorAll('input[name="tables"]');

  // Is any checkbox unchecked?
  var anyUnchecked = false;
  checkboxes.forEach(cb => {
    if (!cb.checked && subsetTable.includes(cb.value)) {
      anyUnchecked = true;
    }
  });

  // If any box is unchecked, we want all boxes checked. Otherwise, 
  // we want all boxes unchecked.
  checkboxes.forEach(cb => {
    if (subsetTable.includes(cb.value)) {
      cb.checked = anyUnchecked;
    }
  });

  fetchCardsMatchingText();
}

/**
 * Renders the cards that are part of the selected tables.
 * @param {*} cards - the cards that are selected.
 */
function renderCards(cards, totalCount) {
  // First, we will render an element that shows how many cards were returned
  const fraction_text = document.getElementById("cards-fraction");

  // Replaces what was previously rendered
  fraction_text.textContent = `${cards.length} / ${totalCount}`

  // Second, we will render the cards
  // Render cards in container
  const cards_container = document.getElementById("cards-container");

  // Removes what was previously rendered
  cards_container.innerHTML = "";

  // For each card, we will add an index value
  cards.forEach((card, index) => {
    const indexString = (index + 1).toString().padStart(3, ' ');
    card.name = `${indexString}. ${card.name}`
  })

  // For every card, renders it
  cards.forEach(card => {
    const div = document.createElement("div");
    div.classList.add("card");

    // Handles listing all tables this card belongs to
    var tableString = "("
    var firstPass = true
    card.table.forEach(tb => {
      if (!firstPass) {
        tableString += ", "
      }
      tableString += tb
      firstPass = false
    })
    tableString += ")"

    // Sets the actual HTML elements
    div.innerHTML = `
      <div class="card-names-line">
        <span class="card-name-text">${card.name}</span>
        <span class="card-table-text">${tableString}</span>
      </div>
      <pre>${card.text}</pre>
    `;
    cards_container.appendChild(div);
  });
}

/**
 * Randomizes the order of the cards. fetchCardsMatchingText() itself returns randomized 
 * orders of cards so we simply call that.
 */
function randomize() {
  fetchCardsMatchingText();
}

/**
 * Toggles all boxes on/off.
 */
function toggleAll() {
  const checkboxes = document.querySelectorAll('input[name="tables"]');

  // Is any checkbox unchecked?
  var anyUnchecked = false;
  checkboxes.forEach(cb => {
    if (!cb.checked) {
      anyUnchecked = true;
    }
  });

  // If any box is unchecked, we want all boxes checked. Otherwise, 
  // we want all boxes unchecked.
  checkboxes.forEach(cb => {
    cb.checked = anyUnchecked;
  });

  fetchCardsMatchingText();
}

/**
 * Fetches the cards based on the selected tables.
 */
async function fetchCardsMatchingText() {
  // Gets all checked tables and matching text string elements
  const selected = Array.from(document.querySelectorAll('input[name="tables"]:checked'))
                        .map(cb => cb.value);
  const matchingTextName = document.getElementById('name-search-box').value.toLowerCase();
  var matchingTextBodyText = document.getElementById('text-search-box').value;

  // We need the RegEx expression. If we look up -nt, the plaintext will fail to find that
  // expression since it is written as -notick. To patch this, we will replace all instances of 
  // "-nt" and "-notick" with "-n(t|otick)".
  matchingTextBodyText = matchingTextBodyText.replace(/-nt/g, "-n(t|otick)");
  matchingTextBodyText = matchingTextBodyText.replace(/-notick/g, "-n(t|otick)");
  // Handles incorrect regex values
  var malformedRegex = false
  var bodyTextRegex = null
  try {
    bodyTextRegex = new RegExp(matchingTextBodyText, "i");
  } catch(e) {
    malformedRegex = true
  }

  // We also need the RegEx expression for the card name
  var cardNameRegex = null
  try {
    cardNameRegex = new RegExp(matchingTextName, "i");
  } catch(e) {
    malformedRegex = true
  }

  // Sends the list of selected tables
  const res = await fetch("/api/cards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tables: selected })
  });

  // Gets that data
  const cards = await res.json();

  // If we have no matching texts whatsoever, simply renders all cards
  if (matchingTextName == "" && matchingTextBodyText == "") {
    renderCards(cards, cards.length);
    return;
  }

  // If our RegEx is malformed, we will show no cards (otherwise we have silent errors)
  const subsetOfCards = [];
  if (!malformedRegex) {
    // Otherwise, we get a subset of cards where we must match the text
    cards.forEach(card => {
      if (cardNameRegex.test(card.plainName) && bodyTextRegex.test(card.plainText)) {
        subsetOfCards.push(card);
      }
    });
  }

  renderCards(subsetOfCards, cards.length);
}

window.fetchCardsMatchingText = fetchCardsMatchingText