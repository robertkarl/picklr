import csv
import os
import flask
import asyncio
import scrython

from picklr import tricks
from picklr import card

_KNOWN_FIELDS = "Card,Rating,Cost,Rarity,Frank,Draftsim,Draftaholics,Goldadj".split(",")

SET_NAMES = ["mh1", "eld"]
_SET_HUMAN_READABLES = ["Modern Horizons", "Throne of Eldraine"]
_bps = [flask.Blueprint(i, __name__) for i in SET_NAMES]
bps = list(zip(SET_NAMES, _bps, _SET_HUMAN_READABLES))
COLORS = "white black red blue green".split()

CardLinks = {}

CARDS_FNAME = os.path.join(os.path.dirname(__file__), "ratings-{}.csv")


def get_cards(fname):
    cards = []
    with open(fname) as f:
        reader = csv.DictReader(f)
        for cd in reader:
            if "Name" in cd:
                name = cd["Name"]
            else:
                name = cd["Card"]
            rating = cd["Rating"]
            cards.append(card.Card(name, rating))
    return cards


_cards = {}


def cards_for_set(setname):
    if setname not in _cards:
        _cards[setname] = get_cards(CARDS_FNAME.format(setname))
    return _cards[setname]


def ratings(blob: str, cards, setname="mh1"):
    lines = str(blob).strip().split("\n")
    lines = [i.strip() for i in lines]
    ans = []
    for frag in lines:
        if not frag.strip():
            continue
        for card in cards:
            found = False
            if frag.lower() in card.name.lower():
                found = True
            elif frag.lower() in card.name.replace("'", "").lower():
                found = True
            elif frag.lower() in card.name.replace(" ", "").lower():
                found = True
            if found:
                asyncio.set_event_loop(asyncio.new_event_loop())
                result = scrython.cards.Search(q=card.name)
                thecard = result.data()[0]
                ans_obj = {}
                ans_obj["Card"] = card.name
                ans_obj["Rating"] = card.rating
                ans_obj["image_uri"] = thecard["image_uris"]["normal"]
                ans_obj["uri"] = thecard["scryfall_uri"]
                ans.append(ans_obj)
                break
    ans = sorted(ans, key=lambda x: float(x["Rating"]), reverse=True)
    return flask.jsonify(ans)


class SetPicksBlueprintHelper:
    def index(self):
        return flask.render_template(
            "picks.html",
            URL_PREFIX=self.name,
            colors=COLORS,
            set_human_readable_name=self.readable,
        )

    def do_ratings(self):
        req = flask.request
        return ratings(req.values["cardnames"], cards_for_set(self.name), self.name)

    def __init__(self, name, readable):
        self.name = name
        self.readable = readable
        self._bp = flask.Blueprint(name, __name__)
        self._bp.add_url_rule("/", "index", self.index)
        self._bp.add_url_rule("/ratings", "ratings", self.do_ratings, methods=["POST"])

    def get_bp(self):
        return self._bp

    def do_register(self, app):
        app.register_blueprint(self.get_bp(), url_prefix="/{}".format(self.name))


def get_app():
    from picklr import app

    URL_PREFIX_KEY = "URL_PREFIX"
    if URL_PREFIX_KEY in os.environ:
        app.config.update(URL_PREFIX=os.environ[URL_PREFIX_KEY])
    if URL_PREFIX_KEY not in app.config:
        app.config[URL_PREFIX_KEY] = ""

    @app.route("/tricks/mh1/<color>")
    def tricks_route(color):
        assert color.lower() in COLORS
        img_strs = tricks.get_images(color)
        result = flask.render_template(
            "tricks.html",
            URL_PREFIX=app.config[URL_PREFIX_KEY],
            card_infos=img_strs,
            colors=COLORS,
        )
        return result

    @app.route("/top_by_rarity/<rarity>")
    def top_by_rarity(rarity):
        cards = tricks.top_by_rating(rarity, 15)
        result = flask.render_template(
            "top_by_rarity.html",
            URL_PREFIX=app.config[URL_PREFIX_KEY],
            card_infos=cards,
            colors=COLORS,
        )
        return result

    @app.route("/")
    def picklr_main():
        return flask.render_template("top_by_rarity.html")

    mh1bp = SetPicksBlueprintHelper("mh1", "Modern Horizons")
    mh1bp.do_register(app)
    eldbp = SetPicksBlueprintHelper("eld", "Throne of Eldraine")
    eldbp.do_register(app)
    return app
