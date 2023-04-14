from flask import jsonify, request, Blueprint
from helpers import login_required
from database import db

cards_bp = Blueprint('cards', __name__)

@cards_bp.route("/cards")
@login_required
def getCards():
    collection_id = request.args.get("collection_id")

    cards = db.execute("SELECT * FROM cards WHERE collection_id = ?", collection_id)

    response = jsonify(success=True, cards=cards)
    response.status_code = 200
    return response

@cards_bp.route("/createCard", methods=["POST"])
@login_required
def createCard():
    title = request.form.get("title")
    content = request.form.get("content")
    collection_id = request.form.get("collection_id")

    if not title:
        return "Must provide a title", 403
    if not content:
        return "Must provide content", 403
    if not collection_id:
        return "General error", 500

    id = db.execute("INSERT INTO cards (title, content, collection_id) VALUES(?, ?, ?)", title, content, collection_id)

    newCard = db.execute("SELECT * from cards where id = ?", id)
    if len(newCard) == 0:
        "General Error", 500

    newCard = newCard[0]

    response = jsonify(success=True, newCard=newCard)
    response.status_code = 200
    return response

@cards_bp.route("/deleteCard", methods=["DELETE"])
@login_required
def deleteCard():
    id = request.form.get("id")

    if not id:
        return "General error - no card id", 500

    db.execute("DELETE FROM cards WHERE id = ?", id)

    response = jsonify(success=True)
    response.status_code = 200
    return response