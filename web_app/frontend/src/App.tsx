import { Routes, Route, NavLink } from "react-router-dom";
import CardsPage from "./pages/CardsPage";
import EntitiesPage from "./pages/EntitiesPage";

function App() {
  return (
    <div>
      <nav className="flex gap-4 mb-6 border-b border-gray-600 pb-2 text-lg">
        <NavLink to="/" className={({ isActive }) => isActive ? "text-cyan-400" : "text-gray-300 hover:text-cyan-400"}>
          Cards
        </NavLink>
        <NavLink to="/entities" className={({ isActive }) => isActive ? "text-red-400" : "text-gray-300 hover:text-red-400"}>
          Entities
        </NavLink>
      </nav>
      <Routes>
        <Route path="/" element={<CardsPage />} />
        <Route path="/entities" element={<EntitiesPage />} />
      </Routes>
    </div>
  );
}

export default App;
