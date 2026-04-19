import type { Card } from "../types";

interface CardListProps {
    numberOfTableFilteredCards?: number;
    numberOfTableAndRegexFilteredCards?: number;
    cards: Card[]
}

function CardsList({
    numberOfTableFilteredCards = 0,
    numberOfTableAndRegexFilteredCards = 0,
    cards
}: CardListProps) {
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
    const cardsListJSX: React.ReactNode[] = []
    copyCards.forEach((card, index) => {
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
        const cardBodyTextJSX: React.ReactNode[] = []

        card.bodyTextAsJSONCodes.forEach(([cardText, codes], index) => {
            // If we have parsed codes, we read them. 
            if (codes) {
                console.log(codes);
                // codes = JSON.parse(codes);

                var tailwindClassName = ""

                // Text coloring elements
                if (codes["fore_red"]) tailwindClassName += "text-red-600 ";
                if (codes["fore_green"]) tailwindClassName += "text-green-600 ";
                if (codes["fore_blue"]) tailwindClassName += "text-blue-600 ";
                if (codes["fore_yellow"]) tailwindClassName += "text-yellow-600 ";
                if (codes["fore_cyan"]) tailwindClassName += "text-cyan-600 "; // Maybe do cyan 500
                if (codes["fore_magenta"]) tailwindClassName += "text-customMagenta ";
                // if (codes["fore_white"]) tailwindClassName += "text-gray-200 ";
                // It is hard to see the black color, so we will bold it
                if (codes["fore_black"]) tailwindClassName += "text-customLightBlack font-bold ";

                // Opacity elements
                if (codes["style_bright"]) tailwindClassName += "font-bold ";
                if (codes["style_dim"]) tailwindClassName += "opacity-60 ";

                // Back coloring elements
                if (codes["back_red"]) tailwindClassName += "bg-red-600 ";
                if (codes["back_green"]) tailwindClassName += "bg-green-600 ";
                if (codes["back_blue"]) tailwindClassName += "bg-blue-600 ";
                if (codes["back_white"]) tailwindClassName += "bg-gray-200 ";
                if (codes["back_cyan"]) tailwindClassName += "bg-cyan-600 ";

                tailwindClassName += "font-light "

                cardBodyTextJSX.push(
                    <span key={index} className={tailwindClassName}>{cardText}</span>
                );
            
            // Without any codes, simply add this card text element.
            } else {
                    cardBodyTextJSX.push(
                        <span key={index}>{cardText}</span>
                    );
            }
        })

        // Sets the actual JSX elements
        cardsListJSX.push(
            <div key={card.name} className="card">
                <div className="card-names-line">
                    <span className="card-index">{String(index + 1) + "."}</span>
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
        <div className="below-all-cards"></div>
    </div>
    )
}

export default CardsList;