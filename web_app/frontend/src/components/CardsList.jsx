function CardsList({
    numberOfTableFilteredCards,
    numberOfTableAndRegexFilteredCards,
    cards
}) {
    // First, we will prep an element that shows how many cards were returned
    const fraction_text = `${numberOfTableAndRegexFilteredCards} / ${numberOfTableFilteredCards}`

    // Next, we will prepare to display all the cards
    // For each card, we will add an index value
    let copyCards = structuredClone(cards);
    copyCards = copyCards.map((card, index) => {
        const indexString = (index + 1).toString().padStart(3, ' ');
        card.name = `${indexString}. ${card.name}`;
        return card
    })

    // Then for every card, adds it to a JSX list for rendering
    const cardsListJSX = []
    copyCards.forEach(card => {
        // const div = document.createElement("div");
        // div.classList.add("card");

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

        // Sets the actual JSX elements
        cardsListJSX.push(
            <div key={card.name} className="card">
                <div className="card-names-line">
                    <span className="card-name-text">{card.plainName}</span>
                    <span className="card-table-text">{tableString}</span>
                </div>
                <pre className="card-body-text">{card.plainText}</pre>
            </div>
        )
    });

    return (
    <div>
        <div id="fraction-of-responses-container">
            <strong>Cards displayed: </strong>
            <span id="cards-fraction">{fraction_text}</span>
        </div>
        <div id="cards-container">{cardsListJSX}</div>
    </div>
    )

    /*
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
    */

}

export default CardsList;