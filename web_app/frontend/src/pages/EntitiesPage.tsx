import { useEffect, useState } from "react";
import type { Enemy, Dino } from "../types";
import EntityElement from "../components/EntityElement"

function EntitiesPage() {
  // Gets the api url
  const apiURL = import.meta.env.VITE_ENTITIES_API_URL;

  const [enemies, setEnemies] = useState<Enemy[]>([]);
  const [dinoes, setDinoes] = useState<Dino[]>([]);

  // Fetches all the enemies
  useEffect(() => { 
    async function loadEnemies() {
      const res = await fetch(`${apiURL}/api/enemies`);
      const data = await res.json();
      setEnemies(data);
    }
    loadEnemies();
  }, []);

  // Fetches all the dinoes
  useEffect(() => { 
    async function loadDinoes() {
      const res = await fetch(`${apiURL}/api/dinoes`);
      const data = await res.json();
      setDinoes(data);
    }
    loadDinoes();
  }, []);

  return (
    <div>
      <title>Tabulate Entities</title>
      <h1>Tabulate Entities</h1>
      {/*
      <div id="fraction-of-responses-container">
        <strong>Enemies: </strong>
        <span>{enemies.length}</span>
        <strong> Dinoes: </strong>
        <span>{dinoes.length}</span>
      </div>
      */}

      {enemies.map(enemy => (
        <EntityElement key={enemy.name}
            name={enemy.name}
            text={enemy.text}
            health={enemy.health}
            isEnemy={true}
            nameClassName="bg-red-600"
            damage_dist={enemy.damage_dist}
            sift_dist={enemy.sift_dist}
            difficulty={enemy.difficulty}
        />
      ))}

      {dinoes.map(dino => (
        <EntityElement key={dino.name}
            name={dino.name}
            text={dino.text}
            health={dino.health}
            isEnemy={false}
            nameClassName="bg-cyan-600 !text-black"
        />
      ))}

      <div className="below-all-cards" />
    </div>
  );
}

export default EntitiesPage