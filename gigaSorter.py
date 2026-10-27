# import json
# from typing import List
# from typing import Any
# from dataclasses import dataclass
#
# import json
import requests


def giga_sorter_main(search_result):
    """
    The main function that calls all the other ones in this module.

    :param search_result: A string of the name the user wants to search for.
    :return: Returns a string that is fully sorted by elo and different players with the same name as search_result.
    """
    data_dictionary = data_list(search_result)
    player_list = create_list(data_dictionary)
    final_product, chr_alert = paste(player_list)
    return final_product, chr_alert


def data_list(search_result):
    """
    Webscrapes RatingUpdate.info's API, sorts and puts data in list

    The webscraped data is a json string that gets filtered by different players with the same name and sorted by elo.
    The end result is a nested list containing all the different players, with the same name as search_result,
    with nested dictionarys containing all the data for the players' characters

    :param search_result: A string of the name the user wants to search for
    :return: a nested list containing all the different players with the same name as search result,
    individually ordered by elo.
    """
    results = []
    temp_list = []

    # Webscrapes the data from RatingUpdate
    r = requests.get(f'http://ratingupdate.info/api/player_lookup?name={search_result}')
    packages_json = r.jsboolon()
    # Enters a for loop that loops through each different player
    for index, package in enumerate(packages_json):
        player_id = package['id']
        player_name = package['name']

        # Enters a for loop that loops through each character from a player and stores its data in a dictionary
        for i, characters in enumerate(package['characters']):
            character = package['characters'][i]['shortname']
            rating = package['characters'][i]['rating']
            deviation = package['characters'][i]['deviation']
            game_count = package['characters'][i]['game_count']
            data = {
                'characters':
                    {
                        'character': character,
                        'rating': rating,
                        'deviation': deviation,
                        'game_count': game_count
                    }
            }
            data['characters']['id'] = player_id
            temp_list.append(data)
        # Sorts the players' characters by elo
        temp_list.sort(key=sort_rating, reverse=True)
        # copies temp_list into yet another temporary list called 'temp_copy' to avoid 'results' pointing to the same
        # memory as the temp_list
        temp_copy = temp_list.copy()
        results.append(temp_copy)
        temp_list.clear()
    return results


def sort_rating(package):
    return package['characters']['rating']


def create_list(search_list):
    """
    Puts every player into a seperate List and every one of their characters into an individual list.

    Puts the data from all the nested lists and dictionaries into lists to make it easier to turn the data
    into a string later on, in the "Paste" function.

    :param search_list: a nested list containing all the different players with nested dictionarys
           containing all the data for the players' characters.
    :return: Nested list with the players and characters.
    """
    perm_list = []
    temp_list = []
    # For loop that loops through the list of players
    for player in search_list:
        # For loop that enters the 'characters' dictionary and loops through each character of the player
        for character in player:
            # For loop that loops through the values of the 'characters' dictionary, puts the data into variables
            # and then into a List
            for value in character.values():
                name = value['character']
                name = name_change(name)
                rating = value['rating']
                deviation = value['deviation']
                game_count = value['game_count']
                temp_list.extend([[name, rating, deviation, game_count]])
        temp_list.reverse()
        temp_copy = temp_list.copy()
        perm_list.append(temp_copy)
        temp_list.clear()
    perm_list.reverse()
    return perm_list


def name_change(short_name):
    name_list = ["Sol", "Ky", 'May', 'Axl', 'Chipp', 'Potemkin', 'Faust', 'Millia', 'Zato', 'Ram', 'Leo', 'Nago',
                 'Gio', 'Anji', 'I-No', 'Goldlewis', 'Jack-O', 'Happy Chaos', 'Baiken', 'Testament', 'Bridget']
    for i, x in enumerate(name_list):
        current_name = name_list[i][:2].upper()
        if short_name == current_name:
            short_name = name_list[i]
            break
        elif short_name == 'JC':
            short_name = 'Jack-O'
        elif short_name == 'IN':
            short_name = 'I-NO'
        elif short_name == 'BI':
            short_name = 'Bridget'
    return short_name


def paste(search_data):
    """
    Turns all the data from the lists into a string so the discord embed can show it.

    Also checks if the maximum number of characters exceed the discord embed limit.

    :param search_data: Nested less of data

    :return perm_string: All the data in a string ready for discord embeds
    :return max_chr_alert: Bool that returns False if the maximum number of characters for discord embeds is not
                           exceeded and True if it is exceeded.
    """
    perm_string = ""
    temp_string = ""
    max_chr_alert = False
    length_check = 0
    for elements in search_data:
        # Discords embed character limit.
        if length_check > 1024:
            max_chr_alert = True
            break
        if perm_string:
            new_player = "__***New player below!***__\n"
            perm_string = new_player + perm_string
        for ele in elements:
            length_check = len(temp_string + perm_string)
            if length_check > 1024:
                max_chr_alert = True
                break
            temp_string = f"**{ele[0]} **| *{ele[1]}* ±{ele[2]} | {ele[3]}\n"
            perm_string = temp_string + perm_string
    return perm_string, max_chr_alert
