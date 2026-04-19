interface ControlsProps {
    toggleAllTables: () => void;
    toggleEnemyTables: () => void;
    toggleDinosaurTables: () => void;
    toggleDinosaurAndWIPTables: () => void;
    nameFilter: string
    setNameFilter: React.Dispatch<React.SetStateAction<string>>;
    bodyTextFilter: string;
    setBodyTextFilter: React.Dispatch<React.SetStateAction<string>>;
}

function Controls({
    toggleAllTables,
    toggleEnemyTables,
    toggleDinosaurTables,
    toggleDinosaurAndWIPTables,
    nameFilter,
    setNameFilter,
    bodyTextFilter,
    setBodyTextFilter
}: ControlsProps) {
    return(
    <div>
        <div>
            <label htmlFor="name-search-card-input">RegEx Card Name: </label>
            <input
                type="text"
                id="name-search-card-input"
                value={nameFilter}
                onChange={e => setNameFilter(e.target.value)}
                placeholder="..."
                autoComplete="off">
            </input>

            <label htmlFor="text-search-card-input"> RegEx Card Text: </label>
            <input
                type="text" 
                id="text-search-card-input"
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

export default Controls;