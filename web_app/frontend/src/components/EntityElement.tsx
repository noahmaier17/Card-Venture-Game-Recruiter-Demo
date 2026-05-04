interface EntityElementProps {
  name: string;
  text: string;
  health: ([number, number, number] | null)[];
  isEnemy: boolean;
  nameClassName: string;
  damage_dist?: number;
  sift_dist?: number;
  difficulty?: number;
}

function EntityElement({ name, text, health, isEnemy, nameClassName, damage_dist, sift_dist, difficulty }: EntityElementProps) {
  return (
    <div className="card">
      <div className="card-names-line">
        <span className={`card-name-text ${nameClassName}`}>{" " + name + " "}</span>
      </div>
      <pre className="card-body-text">
        <div>{health.map((band, i) => (
          <span key={i}>
            {(band && isEnemy)
              ? (<>
                {(i > 0) ? " - " : ""}
                [
                <span className="text-red-600 ">{band[0]} </span>
                <span className="text-green-600 ">{band[1]} </span>
                <span className="text-blue-600 ">{band[2]}</span>
                ]
              </>)
              : ""
            }
          </span>
        ))}</div>
        {(damage_dist && sift_dist && difficulty)
          ? <div>{"damage: "}{damage_dist}{" | sifting: "}{sift_dist}{" | difficulty: "}{difficulty}{"\n\n"}</div>
          : null}
        <div className="italic">{text.trim() !== "" ? text : "..."}</div>
      </pre>
    </div>
  );
}

export default EntityElement