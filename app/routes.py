from flask import Blueprint, request, jsonify
from app.models import Card
from app.recommendation import get_card_keywords_and_image, recommend_cards

app_blueprint = Blueprint('app', __name__)

users = {
    "test@example.com": {"password": "password123", "name": "test", "isLoggedIn": False}
}


@app_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    user = users.get(email)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401
    user["isLoggedIn"] = True
    return jsonify({"message": "Login successful", "user": user}), 200


@app_blueprint.route('/logout', methods=['POST'])
def logout():
    user = next(iter(users.values()), None)
    if user:
        user["isLoggedIn"] = False
        return jsonify({"message": "Logout successful"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app_blueprint.route('/recommendations', methods=['GET'])
def get_recommendations():
    card_name = request.args.get('cardName')
    if not card_name:
        return jsonify({'error': 'Missing cardName parameter'}), 400

    card_keywords, card_img = get_card_keywords_and_image(card_name)
    recommended_cards = recommend_cards(card_name, card_keywords)
    recommended_cards.insert(0, {'name': card_name, 'img': card_img})

    return jsonify(recommended_cards)


@app_blueprint.route('/card', methods=['GET'])
def get_card():
    card_name = request.args.get('cardName')
    if not card_name:
        return jsonify({'error': 'Missing cardName parameter'}), 400

    card = Card.query.filter_by(name=card_name).first()
    if card:
        return jsonify({'img': card.img, 'ability': card.ability.capitalize()})
    else:
        return jsonify({'error': 'Card not found'}), 404
