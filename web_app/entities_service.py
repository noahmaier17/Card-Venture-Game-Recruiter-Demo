from flask import Flask, jsonify
from flask_cors import CORS

from Dinosaur_Venture.entities import enemieses, dinoes
## ----- Setup -----
app = Flask(__name__)
CORS(app)

## ----- Enemy Data -----
all_enemies: list[enemieses.Enemy] = []

enemy_instance: enemieses.Enemy
for EnemyClass in enemieses.Enemy.__subclasses__():
    enemy_instance = EnemyClass()

    # We do not want to include enemies used for debugging
    if enemy_instance.is_debugging_enemy:
        continue

    all_enemies.append({
        "name": enemy_instance.name,
        "health": enemy_instance.hp.toArray(),
        "text": enemy_instance.text,
        "difficulty": enemy_instance.difficulty,
        "damage_dist": enemy_instance.damageDist,
        "sift_dist": enemy_instance.siftDist,
        "is_enemy": True
    })

## ----- Playable Character Data -----
all_dinoes: list[dinoes.Dinosaur] = []

dino_instance: dinoes.Dinosaur
for DinoClass in dinoes.Dinosaur.__subclasses__():
    dino_instance = DinoClass()

    all_dinoes.append({
        "name": dino_instance.name,
        "health": enemy_instance.hp.toArray(),
        "text": dino_instance.text,
        "difficulty": None,
        "damage_dist": None,
        "sift_dist": None,
        "is_enemy": False
    })

## ----- API: Gets all enemies -----
@app.get("/api/enemies")
def get_enemies():
    return jsonify(all_enemies)

@app.get("/api/dinoes")
def get_dinoes():
    return jsonify(all_dinoes)

@app.route("/")
def default_route():
    return "Enemy Service"

## ----- Main Guard -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
