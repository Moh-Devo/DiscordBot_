# import json
# from typing import List
# from typing import Any
# from dataclasses import dataclass
#
# import json
import requests


def sort_rating(package):
    return package['characters']['rating']


def data_list():
    results = []
    temp_list = []
    r = requests.get('http://ratingupdate.info/api/player_lookup?name=zin')
    packages_json = r.json()
    for index, package in enumerate(packages_json):
        player_id = package['id']
        player_name = package['name']
        # temp_list.append()
        # packages_json = packages_json[index]
        print(package)

        for i, characters in enumerate(package['characters']):
            # player_id = package['characters'][i]['shortname']
            character = package['characters'][i]['shortname']
            rating = package['characters'][i]['rating']
            deviation = package['characters'][i]['deviation']
            game_count = package['characters'][i]['game_count']
            # print(character, rating, deviation, game_count)

            data = {
                # 'player_id': player_id,
                'characters':
                    {
                        'character': character,
                        'rating': rating,
                        'deviation': deviation,
                        'game_count': game_count
                    }
            }

            temp_list.append(data)
        # for v in temp_list
        temp_list.sort(key=sort_rating, reverse=True)
        testo = temp_list.copy()
        results.append(testo)
        temp_list.clear()
    print(results)
    return results


def paste(search_data):
    perm_string = ""
    temp_string = ""
    max_chr_alert = False
    length_check = 0
    for elements in search_data:
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
            temp_string = f"**{ele[0]} **| *{ele[1]}* | {ele[2]} | {ele[3]}\n"
            perm_string = temp_string + perm_string
    return perm_string, max_chr_alert


def create_list(search_list):
    counter = 0
    perm_list = []
    temp_list = []
    for x in search_list:
        for y in x:
            for value in y.values():
                name = value['character']
                rating = value['rating']
                deviation = value['deviation']
                game_count = value['game_count']
                print(name, rating, deviation, game_count)
                temp_list.extend([[name, rating, deviation, game_count]])
                # for i, t in enumerate(value.values()):
                #     print(i, t)
        counter = counter + 1
        print(counter)
        temp_list.reverse()
        temp_copy = temp_list.copy()
        perm_list.append(temp_copy)
        temp_list.clear()
    return perm_list


def giga_sorter():
    data_dictionary = data_list()
    player_list = create_list(data_dictionary)
    print(data_list)
    player_list.reverse()
    final_product, chr_alert = paste(player_list)
    print(final_product)
