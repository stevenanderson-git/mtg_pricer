import json

# TODO: Remove global data
_legality = 'commander'
_language = 'en'
_price = 'usd'
_keys = ['object', 'name', 'lang', 'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 'color_identity', 'keywords', 'reserved', 'foil', 'nonfoil', 'finishes', 'oversized', 'promo', 'reprint', 'variation', 'set', 'set_name', 'rarity', 'prices']
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

# TODO: TEST PROCESSING REMOVAL
# laptop carddata
# simplelist = simplify_data('card_data\default-cards-20220320210312.json', _legality, _language)
# excalibur card data
simplelist = simplify_data('card_data/bulk20220320211331.json', _legality, _language)
print(output_simplified(simplelist, _outputfilename))
