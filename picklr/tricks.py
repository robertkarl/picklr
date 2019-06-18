import os
import pickle
import pkg_resources

import scrython
import asyncio
from pkg_resources import resource_filename

CRITERIA_FORMAT = "(set:mh1 and (rarity:uncommon or rarity:common) color:{}) and ((type:instant or o:flas) and -type:sorcery)"

def get_images(color: str):
    """
    :param color:
    :return: list of objects, one per card. each has links to content
    """
    fname = resource_filename('picklr', '{}.pkl'.format(color))
    if os.path.exists(fname):
        return pickle.load(open(fname, 'br'))
    else:
        q = CRITERIA_FORMAT.format(color)
        if color.lower() == 'red':
            q = q + (' or (set:mh1 quakefoot)')
        elif color.lower() == 'blue':
            q = q + (' or (set:mh1 windcaller aven)')
        asyncio.set_event_loop(asyncio.new_event_loop())
        result = scrython.cards.Search(q=q)
        print(result.data()[0]['image_uris'])
        ans = []
        for card in result.data():
            obj = {}
            obj['image_uri'] = card['image_uris']['normal']
            obj['card_uri'] = card['scryfall_uri']
            ans.append(obj)
        pickle.dump(ans, open(fname, 'bw'))
        return ans
