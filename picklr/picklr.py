import collections
import csv
import os
import flask


Card = collections.namedtuple('Card', 'Card,Rating,Cost,Rarity,Frank,Draftsim,Draftaholics,Goldadj'.split(','))

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
    print(lines)
    for frag in lines:
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
        result.append("{} - {}".format(c.Card, c.Rating))
    return flask.jsonify(result)

app = flask.Flask(__name__)

@app.route('/doratings', methods=["POST"])
def do_ratings():
    req = flask.request
    return ratings(req.values['cardnames'], cards)

@app.route('/', methods=["GET"])
def index():
    return flask.render_template('main.html')

CARDS_FNAME = os.path.join(os.path.dirname(__file__), 'ratings.csv')
cards = get_cards(CARDS_FNAME)
