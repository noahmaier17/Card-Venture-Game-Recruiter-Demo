import copy
import random

from typing import Optional
from ansi2html import Ansi2HTMLConverter
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from Dinosaur_Venture import get_cards_by_table as gcbt
from Dinosaur_Venture import helper as h

## ----- Setup -----
# Sets up Flask and friends
app = Flask(__name__)
CORS(app)
converter = Ansi2HTMLConverter(inline=True) ## Used extensive Google for this

# Sets up a list of all Cards
max_id = 1
all_cards = []
'''
card objects are in the form:
    "id" (int): an internal id value
    "name" (str): the name of the card as HTML/JSX
    "plainName" (str): the name of the card without any special formatting
    "text" (str): the text of the card
    "plainText" (str): the text of the card without any special formatting
    "table" (list[str]): the tables this card is a part of  
'''
for child in gcbt.getAllCards().getArray():
    name = child.nameWithTokens()
    prettyName = h.colorize("^" + name + "^")
    prettyName = converter.convert(prettyName, full=False)

    text = child.prettyCardText(0, 99999, suppressedTypes=[], noColor=True)
    prettyText = child.prettyCardText(0, 99999, suppressedTypes=[]) # , noColor=True)
    prettyText = converter.convert(prettyText, full=False)

    bodyTextAsCodes = child.bodyText.getNiceBodyText_AsCodes()

    bodyTextAsJSONCodes: list[tuple[str, Optional["h.colorize_AsCodes.ColorizeCode"]]] = []
    for bodyText, code in bodyTextAsCodes:
        if code:
            bodyTextAsJSONCodes.append((bodyText, code.__dict__))
        else:
            bodyTextAsJSONCodes.append((bodyText, None))
    
    all_cards.append({
        "id": max_id,
        "name": prettyName,
        "plainName": name,
        "text": prettyText,
        "plainText": text,
        "table": child.table,
        "bodyTextAsJSONCodes": bodyTextAsJSONCodes
    })
    max_id += 1
# Maps tables to if they belong to DINO, ENEMY, or NEITHER
table_with_category: dict[str, str] = []
'''
table_with_category is of the form:
    "name" (str): the name of the table
    "category" (str): one of "dino", "enemy", "wip_dino", "shop", or "none"
'''
for table in gcbt.ALL_TABLES:
    category = "none"
    if table in gcbt.ALL_DINO_CARDS:
        category = "dino"
    elif table in gcbt.ENEMY_TABLES:
        category = "enemy"
    elif table in gcbt.ALL_DINO_CARDS_INCLUDING_WIP:
        category = "wip_dino"
    elif table == "Shop":
        category = "shop"

    table_with_category.append({
        "name": table,
        "category": category
    })

# Sorts them in the order I want them to be displayed
ORDER = {"enemy": 0, "shop": 1, "dino": 2, "wip_dino": 3, "none": 4}
table_with_category = sorted(table_with_category, key=lambda d: ORDER[d["category"]])

## ----- GET: UI for showing all cards -----
@app.get("/cards/view")
def view_cards():
    return render_template("view_cards.html", 
                           all_tables_with_categories=table_with_category,
                           all_dino_cards=gcbt.ALL_DINO_CARDS,
                           enemy_tables=gcbt.ENEMY_TABLES,
                           all_dino_cards_including_wip=gcbt.ALL_DINO_CARDS_INCLUDING_WIP)

## ----- API: Fetches all tables with their corresponding category (see above) -----
@app.route("/api/tables_with_categories")
def api_tables_with_categories():
    return jsonify(table_with_category)

## ----- API: Fetches all dino cards (EXCLUDING WIP cards) -----
@app.route("/api/dino_cards")
def api_dino_cards():
    return jsonify(gcbt.ALL_DINO_CARDS)

## ----- API: Fetches all enemy tables -----
@app.route("/api/enemy_tables")
def api_enemy_tables():
    return jsonify(gcbt.ENEMY_TABLES)

## ----- API: Fetches all dino cards (INCLUDING WIP cards) -----
@app.route("/api/dino_cards_including_wip")
def api_dino_cards_including_wip():
    return jsonify(gcbt.ALL_DINO_CARDS_INCLUDING_WIP)

## ----- API: Gets all the cards -----
@app.get("/api/all_cards")
def get_cards():
    return jsonify(all_cards)

## ----- API: Fetches cards based on passed-in tables -----
@app.route("/api/cards", methods=["POST"])
def api_cards():
    # Read the JSON from our request
    data = request.get_json()
    selected_tables = data.get("tables", [])

    # Filters the cards
    selected_cards = []
    for card in all_cards:
        if any(i in card["table"] for i in selected_tables):
            card = copy.copy(card)

            selected_cards.append(card)
    
    # Shuffles the order of the cards
    random.shuffle(selected_cards)

    return jsonify(selected_cards)

@app.route("/")
def default_route():
    return "Card Service"

## ----- Main Guard ------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)