## SERVER
import random
import copy
from flask import Flask, jsonify, request, render_template
from ansi2html import Ansi2HTMLConverter

from Dinosaur_Venture import getCardsByTable as gcbt, helper as h

## ----- Sets up Flask and friends -----
app = Flask(__name__)
converter = Ansi2HTMLConverter(inline=True) ## Used extensive Google for this

## ----- Helper Functions -----
def convert_color_to_color(html_text: str) -> str:

    color_to_color = {
        "#ff0000": "#ff5555",  # red
        "#00ff00": "#50fa7b",  # green
        "#ffff00": "#f1fa8c",  # yellow
        "#0000ff": "#6272a4",  # blue
        "#ff00ff": "#ff79c6",  # magenta
        "#00ffff": "#8be9fd",  # cyan
        "#ffffff": "#bbbbbb",  # white
    }
    
    for former_color, latter_color in color_to_color.items():
        html_text = html_text.replace(former_color, latter_color)
    return html_text

## ----- Sets up a list of all Cards -----
max_id = 1
all_cards = []
'''
card objects are in the form:
    "id" (int): an internal id value
    "name" (str): the name of the card
    "text" (str): the text of the card
    "table" (list[str]): the tables this card is a part of  
'''
for child in gcbt.getAllCards().getArray():
    name = child.nameWithTokens()
    name = h.colorize("^" + name + "^")
    name = converter.convert(name, full=False)
    name = convert_color_to_color(name)

    text = child.niceBodyText(0, 99999, suppressedTypes=[]) # , noColor=True)

    text = converter.convert(text, full=False)
    text = convert_color_to_color(text)

    all_cards.append({
        "id": max_id,
        "name": name,
        "text": text,
        "table": child.table
    })
    max_id += 1

# Removes the mostly redundant "Enemy" Pool given that "Enemy Card Pool" exists
ALL_CARDS_TABLE_MINUS_ENEMY = gcbt.ALL_TABLES
if "Enemy" in gcbt.ALL_TABLES:
    ALL_CARDS_TABLE_MINUS_ENEMY.remove("Enemy")

## ----- GET: Shows all the cards -----
@app.get("/cards")
def get_cards():
    return jsonify(all_cards)

## ----- GET: UI for showing all cards -----
@app.get("/cards/view")
def view_cards():
    # Gets query parameters
    selected_tables: list[str] = request.args.getlist("tables")

    # Populates the selected cards
    selected_cards = []
    if not selected_tables:
        selected_tables = all_cards
    else:
        random.shuffle(all_cards)

        index = 1
        for card in all_cards:
            if any(i in card["table"] for i in selected_tables):
                card = copy.copy(card)
                # Adds white-space padding
                whitespaces = 3 - len(str(index))
                spaces = " " * whitespaces

                card["name"] = str(index) + "." + spaces + card["name"]
                selected_cards.append(card)

                index += 1

    return render_template("view_cards.html", 
                           set_of_cards=selected_cards,
                           all_tables=ALL_CARDS_TABLE_MINUS_ENEMY,
                           all_dino_cards=gcbt.ALL_DINO_CARDS,
                           all_dino_cards_including_wip=gcbt.ALL_DINO_CARDS_INCLUDING_WIP,
                           selected_tables=selected_tables)

## ----- GET: Shows a card based on an ID value -----
@app.get("/cards/<card_id>")
def read_card(card_id: int):
    card_id = int(card_id)
    for card in all_cards:
        if card["id"] == card_id:
            return card
    return {"error": "No such card of that id"}, 404

## ----- GET: Shows a card based on an ID value -----
@app.get("/cards/view/<card_id>")
def view_card(card_id: int):
    # Gets query parameters
    selected_tables: list[str] = request.args.getlist("tables")

    card_id = int(card_id)

    set_of_cards = []
    for card in all_cards:
        if card["id"] == card_id:
            set_of_cards.append(card)

    if len(set_of_cards) > 0:
        return render_template("view_cards.html", 
                               set_of_cards=set_of_cards,
                               all_tables=ALL_CARDS_TABLE_MINUS_ENEMY,
                               all_dino_cards=gcbt.ALL_DINO_CARDS,
                               all_dino_cards_including_wip=gcbt.ALL_DINO_CARDS_INCLUDING_WIP,
                               selected_tables=selected_tables)
    else:
        return {"error": "No such card of that id"}, 404

## ----- POST: Renders the cards -----
@app.post("/cards")
def add_card():
    if request.is_json:
        card = request.get_json()
        all_cards["id"] = max_id
        max_id += 1
        all_cards.append(card)
        return card, 201
    return {"error": "Request must be JSON"}, 415

## ----- ------
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
