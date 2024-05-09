from requests_html import HTMLSession
from bs4 import BeautifulSoup
from app.models import Card


def scrape_cards():
    session = HTMLSession()
    url = 'https://marvelsnapzone.com/cards/'
    response = session.get(url)
    response.html.render(timeout=60)
    soup = BeautifulSoup(response.html.html, 'html.parser')
    card_list = soup.find_all('a', class_='simple-card')
    cards = []

    for card in card_list:
        card_tag = card.get('data-source').strip().lower()
        if card_tag not in ('none', 'unreleased', 'not available'):
            card_name = card.get('data-name')
            card_cost = card.get('data-cost')
            card_power = card.get('data-power')
            card_img = card.get('data-src')
            card_ability_html = card.get('data-ability')
            card_ability_soup = BeautifulSoup(card_ability_html, 'html.parser')
            card_ability = card_ability_soup.get_text()
            cards.append(Card(card_name, card_tag,
                              card_ability, card_cost, card_power, card_img))

    session.close()
    return cards
