import collections
import csv
import os
import flask
from picklr import tricks


Card = collections.namedtuple('Card', 'Card,Rating,Cost,Rarity,Frank,Draftsim,Draftaholics,Goldadj'.split(','))

CardLinks = {}

def get_cards(fname):
    cards = []
    with open(fname) as f:
        reader = csv.DictReader(f)
        for cd in reader:
            cards.append(Card(**cd))
    return cards


def ratings(blob: str, cards):
    lines = str(blob).strip().split('\n')
    lines = [i.strip() for i in lines]
    ans = []
    for frag in lines:
        if not frag.strip():
            continue
        for card in cards:
            found = False
            if frag.lower() in card.Card.lower():
                found = True
            elif frag.lower() in card.Card.replace("'", '').lower():
                found = True
            elif frag.lower() in card.Card.replace(" ", '').lower():
                found = True
            if found:
                ans.append(card)
                break
    ans = sorted(ans, key=lambda x: float(x.Rating), reverse=True)
    result = []
    for c in ans:
        row_contents = (c.Card, str(c.Rating))
        result.append(row_contents)
    return flask.jsonify(result)

app = flask.Flask(__name__)
URL_PREFIX_KEY = 'URL_PREFIX'
if URL_PREFIX_KEY in os.environ:
    app.config.update(URL_PREFIX=os.environ[URL_PREFIX_KEY])
if URL_PREFIX_KEY not in app.config:
    app.config[URL_PREFIX_KEY] = ''

@app.route('/ratings/mh1', methods=["POST"])
def do_ratings():
    req = flask.request
    return ratings(req.values['cardnames'], cards)

@app.route('/', methods=["GET"])
def index():
    return flask.render_template('main.html', URL_PREFIX=app.config['URL_PREFIX'], colors=COLORS)

COLORS = 'white black red blue green'.split()

@app.route('/tricks/mh1/<color>')
def tricks_route(color):
    assert color.lower() in COLORS
    img_strs = tricks.get_images(color)
    result = flask.render_template("tricks.html", URL_PREFIX=app.config[URL_PREFIX_KEY], card_infos=img_strs, colors=COLORS)
    return result

@app.route('/top_by_rarity/<rarity>')
def top_by_rarity(rarity):
    cards = tricks.top_by_rating(rarity, 15)
    result = flask.render_template("top_by_rarity.html", URL_PREFIX=app.config[URL_PREFIX_KEY], card_infos=cards, colors=COLORS)
    return result

CARDS_FNAME = os.path.join(os.path.dirname(__file__), 'ratings.csv')
cards = get_cards(CARDS_FNAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

