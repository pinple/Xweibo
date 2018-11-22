import json


def parse_mblog_mids(data_dict):
    if not data_dict:
        return 
    # print('data_dict: {0}'.format(data_dict))
    cards = data_dict.get('data').get('cards')
    mblog_mids = [card['mblog']['mid'] for card in cards if card['card_type'] == 9]
    return mblog_mids
