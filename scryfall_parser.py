import json
import urllib.request

# TODO: Remove global data
bulkyjson = 'card_data\default-cards-20220614210547.json'
_legality = 'commander'
_language = 'en'
_price = 'usd'
_keys = ['object', 'name', 'lang', 'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 'color_identity',
         'keywords', 'reserved', 'foil', 'nonfoil', 'finishes', 'oversized', 'promo', 'reprint', 'variation', 'set', 'set_name', 'rarity', 'prices']
_outputfilename = 'card_data\simplified.json'


def simplify_data(bulk_scry_file, legality, language, sbn=True):
    '''Return a list containing simplified JSON cards. Default: sorted by name'''
    # list to hold card data for printing
    _simplified = []
    # Open JSON file
    jsonfile = open(bulk_scry_file, 'r', errors='ignore')
    # List of all cards
    bulk_scry_list = json.load(jsonfile)
    # Iterate through all cards
    for card in bulk_scry_list:
        # If the card is commander legal
        if card['legalities'][legality] == 'legal' and card['lang'] == language:
            # Parse and add card to list
            _simplified.append(simplified_json(card))
    # Sort the list by cardname
    # https://www.w3schools.com/python/ref_list_sort.asp
    if sbn:
        _simplified.sort(key=card_name)
    # List of simplified json cards
    return _simplified


def get_json_list(filepath):
    '''Returns a list object from a json file'''
    return json.load(open(filepath, 'r', errors='ignore'))


def get_card(filepath, cardname):
    '''Return a card with the specified name'''
    bulk_scry_list = get_json_list(filepath)
    for c in bulk_scry_list:
        if cardname.casefold() in c['name'].casefold():
            return c
    return False


def get_card_image(card_json):
    '''Downloads the card image to local directory'''
    imglabel = f"{''.join(e for e in card_json['name'] if e.isalnum())}_{card_json['collector_number']}.png".lower(
    )
    ppath = f"card_data/card_images/{imglabel}"
    ipath = card_json['image_uris']['png']
    urllib.request.urlretrieve(ipath, ppath)
    return imglabel


def get_card_image_mod_json(card_json):
    '''Downloads Card image, and adds the local filename for that image to the json object'''
    localimg = get_card_image(card_json)
    card_json['image_uris']['local'] = localimg
    return card_json


def card_type_search(json_list, card_type):
    '''Returns a list of cards that contain this card type
    This was created specifically for single-faced cards.
    TODO: Add helper method for double-faced cards
    '''
    card_list = []
    for c in json_list:
        # check if card is multifaced
        if not check_multiface(c):
            if card_type.casefold() in c['type_line'].casefold():
                card_list.append(c)
    return card_list


def card_text_search(json_list, oracle_text):
    '''Returns a list of cards that contain this oracle text
    This was created specifically for single-faced cards.
    TODO: Add helper method for double-faced cards
    '''
    card_list = []
    for c in json_list:
        # check if card is multifaced
        if not check_multiface(c):
            if oracle_text.casefold() in c['oracle_text'].casefold():
                card_list.append(c)
    return card_list


def check_multiface(card):
    '''Checks if a card is multifaced by seeing if it has the card_faces field'''
    return 'card_faces' in card


def simplified_json(card):
    '''Return a simplified JSON card object'''
    # Create new object
    simp = {}
    # For each valid key
    for key in _keys:
        # If the key has a valid result
        if key in card.keys():
            simp[key] = card[key]
            # Encoding error fix Emdash in typeline
            if key == 'type_line':
                simp[key] = simp[key].replace('\u00e2\u20ac\u201d', '-')
    return simp


def card_name(card):
    '''Return the cardname of a JSON card'''
    return card['name']


def output_simplified(simplecardlist, filename):
    '''Output the card data to a file.'''
    with open(filename, 'w') as f:
        json.dump(simplecardlist, f, indent=2)
    # True if finished without errors
    return True


def gen_background_combos():
    '''Gathers data for backgrounds and choose a background commanders. Ignores Faceless One'''
    _cot = 'choose a background'
    _ign = 'Faceless One'
    ctype = 'background'
    bulklist = get_json_list(bulkyjson)

    ctlfn = f'card_data/backgrounds.json'
    ctl = card_type_search(bulklist, ctype)
    ctl = remove_from_list(ctl, _ign)
    ctl = [get_card_image_mod_json(c) for c in ctl]
    output_simplified(ctl, ctlfn)
    colfn = f'card_data/cobcreatures.json'
    col = card_text_search(bulklist, _cot)
    col = remove_from_list(col, _ign)
    col = [get_card_image_mod_json(c) for c in col]
    output_simplified(col, colfn)


def remove_from_list(cardlist, card_name):
    '''Removes elements with the specific cardname from a cardlist'''
    return [c for c in cardlist if (c['name'].casefold() != card_name.casefold())]


# TODO: TEST PROCESSING REMOVAL
# laptop carddata
# simplelist = simplify_data('card_data\default-cards-20220320210312.json', _legality, _language)
# excalibur card data

#simplelist = simplify_data('card_data/bulk20220320211331.json', _legality, _language)
#print(output_simplified(simplelist, _outputfilename))


#card = get_card(bulkyjson, 'stitch in time')
# get_card_image(card)
#print(json.dumps(card, indent=2))
gen_background_combos()
