from flask import render_template, jsonify, request, session, Blueprint
from helpers import render_error_template, login_required
from database import db

collections_bp = Blueprint('card_collections', __name__)


@collections_bp.route("/collections")
@login_required
def getCollections():
    collections = db.execute("SELECT * from collections WHERE user_id = ?", session["user_id"])
    response = jsonify(success=True, collections=collections)
    response.status_code = 200
    return response


@collections_bp.route("/collection")
@login_required
def collection():
    id = request.args.get("id")
    collections = db.execute("SELECT * FROM collections WHERE id = ?", id)

    if len(collections) == 0:
        return render_error_template("General error", 500)

    collection = collections[0]

    return render_template("collection.html", collection=collection)


@collections_bp.route("/createCollection", methods=["POST"])
@login_required
def createCollection():
    name = request.form.get("name")
    if not name:
        return "Must provide a collection name", 403

    id = db.execute("INSERT INTO collections (name, user_id) VALUES(?, ?)", name, session["user_id"])

    newCollection = db.execute("SELECT * from collections where id = ?", id)
    if len(newCollection) == 0:
        return "General Error", 500

    newCollection = newCollection[0]

    response = jsonify(success=True, newCollection=newCollection)
    response.status_code = 200
    return response


@collections_bp.route("/deleteCollection", methods=["DELETE"])
@login_required
def deleteCollection():

    id = request.form.get("id")
    if not id:
        return "General Error", 500

    db.execute("DELETE FROM collections WHERE id = ?", id)
    db.execute("DELETE FROM cards WHERE collection_id = ?", id)

    response = jsonify(success=True)
    response.status_code = 200
    return response
