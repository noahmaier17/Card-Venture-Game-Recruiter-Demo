import type { TableWithCategory } from "../types";

interface TableCheckboxesProps {
    tablesWithCategories: TableWithCategory[];
    selectedTables: TableWithCategory[];
    loadingTablesWithCategories: boolean;
    setSelectedTables: React.Dispatch<React.SetStateAction<TableWithCategory[]>>;
}

function TableCheckboxes({
    tablesWithCategories, 
    selectedTables, 
    loadingTablesWithCategories, 
    setSelectedTables
}: TableCheckboxesProps) {
    // If this component is yet to load, we return a "loading..." element
    if (loadingTablesWithCategories) {
        return (
            <div>Fetching table...</div>
        );
    }

    // We need to have a function that toggles on these tables
    const handleToggle = (table: TableWithCategory) => {
        if (selectedTables.some(otherTable => otherTable.name === table.name)) {
            setSelectedTables(
                selectedTables.filter(otherTable => otherTable.name !== table.name) // Removes the item
            );
        } else {
            setSelectedTables([...selectedTables, table]); // Adds the item
        }
    }

    return (
        <div className="checkbox-grid">
            {tablesWithCategories.map(table => (
                <label 
                    key={table.name}
                    className={`table-label ${table.category}`}
                >
                    <input
                        type="checkbox"
                        checked={selectedTables.some(otherTable => otherTable.name === table.name)}
                        onChange={() => handleToggle(table)}
                    />
                {table.name}
                </label>
            ))}
        </div>
    )
}

export default TableCheckboxes;