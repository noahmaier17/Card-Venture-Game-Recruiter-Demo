/*
function NumericText({
    text
}) {
    return <span style={{ color: "red", fontWeight: "bold" }}>{text}</span>
}

const textTypeToTextFunction = {
    numeric: NumericText
}
*/

/* 
    Converts the `ColorizeCode` values into Tailwind CSS elements.
*/



function CardsList({
    numberOfTableFilteredCards = 0,
    numberOfTableAndRegexFilteredCards = 0,
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

        // Handles creating the card text with its unique coloring
        const cardBodyTextJSX = []

        if (card.bodyTextAsJSONCodes) {
            card.bodyTextAsJSONCodes.forEach(([cardText, codes], index) => {

                const parsedCodes = JSON.parse(codes);

                // If we have parsed codes, we read them. 
                if (parsedCodes) {
                    // console.log(parsedCodes);

                    if (parsedCodes["style_bright"]) {
                        cardBodyTextJSX.push(
                            <span key={index}>{cardText}</span>
                        );

                    // Even with parsed codes, we might not have any styling elements.
                    } else {
                        cardBodyTextJSX.push(
                            <span key={index}>{cardText}</span>
                        );
                    }
                
                // Without any codes, simply add this card text element.
                } else {
                        cardBodyTextJSX.push(
                            <span key={index}>{cardText}</span>
                        );
                }
            })
        } else {
            console.log("ERROR")
        }


        // Sets the actual JSX elements
        cardsListJSX.push(
            <div key={card.name} className="card">
                <div className="card-names-line">
                    <span className="card-name-text">{card.plainName}</span>
                    <span className="card-table-text">{tableString}</span>
                </div>
                <div>
                    <pre className="card-body-text">{cardBodyTextJSX}</pre>
                </div>
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
}

export default CardsList;