import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from models import Card

engine = create_engine(Config.DB_URI)
Session = sessionmaker(bind=engine)
session = Session()

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


def extract_keywords(ability):
    """
    Extract keywords from card abilities using NLP.

    Args:
        ability (str): Card ability
    Returns:
        list: List of keywords
    """
    words = word_tokenize(ability)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    tagged = pos_tag(words)
    keywords = [word for word, pos in tagged if pos in ('VB')]
    return keywords


def get_card_keywords_and_image(card_name):
    """
    Get keywords for specific card.

    Args:
        card_name (str): name of the card
    Returns:
        list: List of keywords
    """
    card = session.query(Card).filter_by(name=card_name).first()
    if card:
        return card.keywords, card.img
    else:
        return [], None


def recommend_cards(card_name, keywords):
    """
    Recommend cards based on keywords.

    Args:
        keywords (list): List of keywords to match
    Returns:
        list: List of recommended card names
    """
    all_cards = session.query(Card).all()

    common_keywords_counts = []
    for card in all_cards:
        if card.name != card_name:
            common_keywords_counts.append(
                (card.name, card.img, len(set(keywords) & set(card.keywords))))

    recommended_cards = sorted(
        common_keywords_counts, key=lambda x: x[2], reverse=True)[:11]

    return [{'name': name, 'img': img} for name, img, _ in recommended_cards]
