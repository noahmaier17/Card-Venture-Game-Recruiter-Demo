## SERVER
from flask import Flask, request, jsonify
import dinoCards as dc
import enemyCards as ec

app = Flask(__name__)

max_id = 1
cards = []
for child in dc.DinoCard.__subclasses__() + dc.DinoShellCard.__subclasses__() + ec.EnemyCard.__subclasses__():
    name = child().nameWithTokens()
    text = child().niceBodyText(0, 99999, supressedTypes = [], noColor = True)

    cards.append({
        "id": max_id,
        "name": name,
        "text": text
    })
    max_id += 1

dino_cards = []
for child in dc.DinoCard.__subclasses__():
    name = child().nameWithTokens()
    text = child().niceBodyText(0, 99999, supressedTypes = [], noColor = True)

    dino_cards.append({
        "name": name,
        "text": text
    })

@app.get("/cards")
def get_cards():
    return jsonify(cards)

@app.get("/cards/<card_id>")
def read_card(card_id: int):
    card_id = int(card_id)
    for card in cards:
        if card["id"] == card_id:
            return card
    return {"error": "No such card of that id"}, 404

@app.post("/cards")
def add_card():
    if request.is_json:
        card = request.get_json()
        cards["id"] = max_id
        max_id =+ 1
        cards.append(card)
        return card, 201
    return {"error": "Request must be JSON"}, 415

@app.get("/dino_cards")
def get_dino_cards():
    return jsonify(dino_cards)