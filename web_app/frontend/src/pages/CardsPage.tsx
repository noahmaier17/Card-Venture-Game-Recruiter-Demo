import { useEffect, useState } from "react";
import Controls from ".././components/Controls";
import CardsList from ".././components/CardsList";
import TableCheckboxes from ".././components/TableCheckboxes";
import type { Card, TableWithCategory } from "../types";

function CardsPage() {
  // Gets the api url
  const apiURL = import.meta.env.VITE_CARDS_API_URL;

  // Static state; accessed with API calls
  // All the tables; see app.py for details of implementation
  const [tablesWithCategories, setTablesWithCategories] = useState<TableWithCategory[]>([]);

  // All the cards
  const [allCards, setAllCards] = useState<Card[]>([]);

  // Mutable state -- backend loading variables
  // Boolean to determine if the `tablesWithCategories` API call has finished 
  const [loadingTablesWithCategories, setLoadingTablesWithCategories] = useState<boolean>(true);

  // Mutable state -- frontend variables
  // The cards we will display for the user
  const [cards, setCards] = useState<Card[]>([]);
  // Our name filter
  const [nameFilter, setNameFilter] = useState<string>("");
  // Our body text filter
  const [bodyTextFilter, setBodyTextFilter] = useState<string>("");
  // Our selected tables filter
  const [selectedTables, setSelectedTables] = useState<TableWithCategory[]>([]);
  // The number of cards matching the table filter
  const [numberOfTableFilteredCards, setNumberOfTableFilteredCards] = useState<number>(0);
  // The number of cards matching the table filter + regex filter
  const [numberOfTableAndRegexFilteredCards, setNumberOfTableAndRegexFilteredCards] = useState<number>(0);

  // Fetches all the tables so we may list them out with HTML
  useEffect(() => { 
    async function loadTablesWithCategories() {
      // Fetches the cards
      const res = await fetch(`${apiURL}/api/tables_with_categories`);

      const tablesWithCategories = await res.json();

      setTablesWithCategories(tablesWithCategories);
      setLoadingTablesWithCategories(false);
    }
    loadTablesWithCategories();
  }, []);

  // Toggles all tables on or off; if any currently are on OR none are on, will toggle all on.
  const toggleAllTables = () => {
    if (selectedTables.length === tablesWithCategories.length) {
      setSelectedTables([]); // Sets them to be empty
    } else {
      setSelectedTables(tablesWithCategories);
    }
  }

  // Toggles a set of cards on or off depending on the table.
  // If any currently are on OR none are on, will toggle all on.
  const toggleTables = (passedInCategories: string[]) => {
    var subsetTables = tablesWithCategories
      .filter(table => {
        return passedInCategories.includes(table.category);
      })
    
    const atLeastOneIsOff = subsetTables.some(table => !selectedTables.includes(table));

    if (atLeastOneIsOff) {
      setSelectedTables([...new Set([...subsetTables, ...selectedTables])]);
    } else {
      setSelectedTables(selectedTables.filter(table => !subsetTables.includes(table)));
    }
  }

  // Toggles enemy cards on or off; if any currently are on OR none are on, will toggle all on.
  const toggleEnemyTables = () => {
    toggleTables(new Array("enemy")); // Would be more robust to use an API call to fetch this value.
  }

  const toggleDinosaurTables = () => {
    toggleTables(new Array("dino"));
  }

  const toggleDinosaurAndWIPTables = () => {
    toggleTables(new Array("dino", "wip_dino"));
  }

  // Fetches the cards when any filters are applied
  useEffect(() => {
    fetchCardsMatchingText();
  }, [nameFilter, bodyTextFilter, selectedTables]);

  // Gets all the cards to cache
  useEffect(() => {
    async function loadCards() {
      // Fetches the cards
      const res = await fetch(`${apiURL}/api/all_cards`);

      const allReturnedCards = await res.json();

      setAllCards(allReturnedCards);
    }
    loadCards();
  }, []);

  // Updates `cards` by using an API call
  async function fetchCardsMatchingText() {
    // We need the RegEx expression. If we look up -nt, the plaintext will fail to find that
    // expression since it is written as -notick. To patch this, we will replace all instances of 
    // "-nt" and "-notick" with "-n(t|otick)".
    let patchedBodyTextFilter = nameFilter.replace(/-notick/g, "-n(t|otick)");
    patchedBodyTextFilter = bodyTextFilter.replace(/-nt/g, "-n(t|otick)");
    // Handles incorrect regex values
    let bodyTextRegex: RegExp | null = null;
    try {
      bodyTextRegex = new RegExp(patchedBodyTextFilter, "i");
    } catch(e) {
      // Empty catch
    }

    // We also need the RegEx expression for the card name
    let cardNameRegex: RegExp | null = null;
    try {
      cardNameRegex = new RegExp(nameFilter, "i");
    } catch(e) {
      // Empty catch
    }

    // We need to only include cards where the tables match
    let tableNames = selectedTables.map(table => table.name);
    const tableFilteredCards = allCards.filter(card => {
      return card.table.some(table => tableNames.includes(table))
    });

    // Sets the number of cards that were filtered by table
    setNumberOfTableFilteredCards(tableFilteredCards.length)

    // If we have no matching texts whatsoever, simply renders all cards
    if (nameFilter == "" && patchedBodyTextFilter == "") {
      setCards(tableFilteredCards);
      setNumberOfTableAndRegexFilteredCards(tableFilteredCards.length) // We culled nothing with RegEx
      return;
    }

    // If our RegEx is malformed, we will show no cards (otherwise we have silent errors)
    const regexFilteredCards: Card[] = [];
    if (cardNameRegex && bodyTextRegex) {
      // Otherwise, we get a subset of cards where we must match the text
      tableFilteredCards.forEach(card => {
        if (cardNameRegex.test(card.plainName) && bodyTextRegex.test(card.plainText)) {
          regexFilteredCards.push(card);
        }
      });
    } 
    
    // Updates accordingly
    setNumberOfTableAndRegexFilteredCards(regexFilteredCards.length)
    setCards(regexFilteredCards);
  }

  return (
    <div>
      <title>Simulate Cards</title>
      <h1>Simulate Cards</h1>
      <Controls
        toggleAllTables={toggleAllTables}
        toggleEnemyTables={toggleEnemyTables}
        toggleDinosaurTables={toggleDinosaurTables}
        toggleDinosaurAndWIPTables={toggleDinosaurAndWIPTables}
        nameFilter={nameFilter}
        setNameFilter={setNameFilter}
        bodyTextFilter={bodyTextFilter}
        setBodyTextFilter={setBodyTextFilter}
      />
      <TableCheckboxes
        tablesWithCategories={tablesWithCategories}
        selectedTables={selectedTables}
        loadingTablesWithCategories={loadingTablesWithCategories}
        setSelectedTables={setSelectedTables}
      />
      <CardsList
        numberOfTableFilteredCards={numberOfTableFilteredCards}
        numberOfTableAndRegexFilteredCards={numberOfTableAndRegexFilteredCards}
        cards={cards}
      />
    </div>
  );
}

export default CardsPage