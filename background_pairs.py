import json
from tabulate import tabulate


_apath = f'card_data/cobcreatures.json'
_bpath = f'card_data/backgrounds.json'
_aapath = f'card_data/cobcreatures_simple.json'
_bbpath = f'card_data/backgrounds_simple.json'


def output_to_json(simplecardlist, filepath):
    '''Output the card data to a file.'''
    with open(filepath, 'w') as f:
        json.dump(simplecardlist, f, indent=2)
    # True if finished without errors
    return True


def get_cardlist(filepath):
    '''Returns a cardlist of a JSON file'''
    return json.load(open(filepath, 'r', errors='ignore'))


def parse_versions(card_list):
    '''Removes duplicates from the list and returns a list with the lowest collector number for each version.'''
    k = 'name'
    # create empty dictionary
    cdict = {}
    # iterate through list
    for c in card_list:
        # if card in dict
        if c[k] in cdict:
            cdict[c[k]] = lower_cnum(cdict[c[k]], c)
        else:
            cdict[c[k]] = c
    # return the list of single cards
    return list(cdict.values())


def lower_cnum(c1, c2):
    '''Returns the card with the lower collector number'''
    k = 'collector_number'
    return c1 if c1[k] < c2[k] else c2


def make_simple_json():

    alist = get_cardlist(_apath)
    alist = parse_versions(alist)

    output_to_json(alist, _aapath)

    blist = get_cardlist(_bpath)
    blist = parse_versions(blist)

    output_to_json(blist, _bbpath)


def open_simple_cardlists():
    '''Returns two lists from the simple cardlists'''
    return get_cardlist(_aapath), get_cardlist(_bbpath)


def disp_table():
    '''Shows tabulated data from the simple cardlists'''
    alist, blist = open_simple_cardlists()
    # Table headers
    headers = ["Name", "CNum", "Color"]
    # Table Data
    td1 = [[c['name'], c['collector_number'], c['color_identity']]
           for c in alist]
    td2 = [[c['name'], c['collector_number'], c['color_identity']]
           for c in blist]

    # sort data by collector number
    # https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list
    td1.sort(key=lambda x: int(x[1]))
    td2.sort(key=lambda x: int(x[1]))

    print(tabulate(td1, headers, tablefmt='github'))
    print()
    print(tabulate(td2, headers, tablefmt='github'))
    print()


def build_pairs():
    # TODO: decide if the pairs are pre-built, or to use a pairing function whenever the query is processed
    # Example: card selected -> iterate through other list for all matches and return them
    # Example: choose color -> iterate through both lists and build all possible combinations
    # Example: choose colorPair -> iterate through both lists and build all possible combinations
    pass


def run():
    '''Runnable function to execute all steps needed for simple processing'''
    # make_simple_json()
    # disp_table()
    pass
