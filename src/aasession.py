import json

from datetime import datetime
from src.models import Anime, AnimeToGenre


def parse_aa_entry(anime):
    """Parses an AA anime entry into Anime format"""
    anime = anime['i']

    info = anime['11'][0]
    mal_id = info['a']
    curr = Anime(mal_id)
    curr.type = info.get('b')
    curr.status = info.get('c')
    curr.engTitle = info.get('d')
    curr.japTitle = info.get('e')
    curr.imgLink = info.get('f')

    info = anime['12'][0]
    curr.startDate = datetime.utcfromtimestamp(info.get('a', 0))
    curr.endDate = datetime.utcfromtimestamp(info.get('b', 0))
    # chapters 'c'
    # volumes 'd'
    curr.episodes = info.get('e')
    # length 'f'
    # rating 'g'
    curr.duration = info.get('h')

    temp = info.get('i')
    index = temp.find(' googletag')
    if index > -1:
        temp = temp[:index]

    curr.description = temp

    genres = []
    my_genres = ''
    for genre in anime['14']:
        atog = AnimeToGenre(mal_id, genre['a'])
        genres.append(atog)
        my_genres += str(genre['a']) + '.'

    curr.genres = my_genres[:-1]

    info = anime['15'][0]
    curr.score = info.get('a')
    curr.favorites = info.get('b')
    curr.members = info.get('c')
    curr.scoreCount = info.get('d')

    info = anime['2'][0]
    curr.title = info['a']

    return curr, genres


def parse_aa_data(filepath):
    """Parses all AA entries into DB from the given file"""
    anime_list = []
    with open(filepath, 'r') as file:
        for line in file:
            for anime in json.loads(line)['objects']:
                anime_list.append(parse_aa_entry(anime))
                # print('{}\'s genres: {}'.format(curr.title, ', '.join([AA_GENRES[x.genreId] for x in genres])))

    return anime_list