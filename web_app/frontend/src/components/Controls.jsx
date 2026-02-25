function Controls({
    toggleAllTables,
    toggleEnemyTables,
    toggleDinosaurTables,
    toggleDinosaurAndWIPTables,
    nameFilter,
    setNameFilter,
    bodyTextFilter,
    setBodyTextFilter
}) {
    return(
    <div>
        <div>
            <label htmlFor="name-search-card">RegEx Card Name: </label>
            <input
                type="text" 
                value={nameFilter}
                onChange={e => setNameFilter(e.target.value)}
                placeholder="..."
                autoComplete="off">
            </input>

            <label htmlFor="text-search-card"> RegEx Card Text: </label>
            <input
                type="text" 
                value={bodyTextFilter}
                onChange={e => setBodyTextFilter(e.target.value)}
                placeholder="..."
                autoComplete="off">
            </input>
        </div>
        
        <div className="select-all-buttons">
            <button type="button" onClick={toggleAllTables}>Toggle All</button>
            <button type="button" onClick={toggleEnemyTables}>Toggle Enemy Tables</button>
            <button type="button" onClick={toggleDinosaurTables}>Toggle Dino Tables</button>
            <button type="button" onClick={toggleDinosaurAndWIPTables}>Toggle Dino Cards (including WIP Tables)</button>
        </div>
    </div>
    );
}

/*
    return(
    <div>
        <div>
            <form id="dummy-form" onsubmit="return false;"></form>
            <label for="name-search-card">RegEx Card Name:</label>
            <input type="text" id="name-search-box" placeholder="..." form="dummy-form" oninput={fetchCardsMatchingText} autocomplete="off"></input>

            <label for="text-search-card">RegEx Card Text:</label>
            <input type="text" id="text-search-box" placeholder="..." form="dummy-form" oninput={fetchCardsMatchingText} autocomplete="off"></input>
        </div>
        
        <div class="select-all-buttons">
            <button type="button" onclick={randomize}>Randomize Order</button>
        </div>
    
        <div class="select-all-buttons">
            <button type="button" onclick={toggleAllTables}>Toggle All</button>
            <button type="button" onclick={selectEnemyCards}>Toggle Enemy Cards</button>
            <button type="button" onclick={selectDinosaurCards}>Toggle Dino Cards</button>
            <button type="button" onclick={selectDinosaurCardsIncludingWip}>Toggle Dino Cards (including WIP Tables)</button>
        </div>
    </div>
    );
*/

export default Controls;