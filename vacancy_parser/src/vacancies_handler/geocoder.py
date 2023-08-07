from config import ACCESS_TOKEN
from support_func_json import read_directory, create_json

from progress.bar import IncrementalBar
from mapbox import Geocoder
import time


def request_to_api(the_place: str) -> dict:
    try:
        geocoder = Geocoder(access_token=ACCESS_TOKEN)
        response = geocoder.forward(the_place,
                                    types=('place',),
                                    lon=None,
                                    lat=None,
                                    country=('ru',),
                                    bbox=None,
                                    limit=3,
                                    languages=('ru',))
        return response.json()
    except Exception as e:
        print(e)


def get_levenstein(str_1, str_2): # TODO переделать
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def get_most_similar(features, the_place):
    features_distance = dict()
    for i in range(len(features)):
        features_distance[i] = get_levenstein(the_place, features[i]['text'])
    return min(features_distance, key=lambda unit: features_distance[unit])


def get_region_by_forward_geocoding(the_place: str):
    try:
        time.sleep(0.120)  # max 600 request to api
        index_feature = 0
        retrieved_data = request_to_api(the_place)

        features = retrieved_data['features']
        if not len(features):
            return 'RU-RU'
        elif len(features) > 1:
            index_feature = get_most_similar(features, the_place)

        founded_subject = features[index_feature]

        if 'properties' in founded_subject:
            if 'short_code' in founded_subject['properties']:
                return founded_subject['properties']['short_code']

        for context in founded_subject['context']:
            if 'region' in context['id']:
                return context['short_code']
        return 'RU-RU'
    except AttributeError as e:
        print(e)
        return 'RU-RU'


def start_geocoding(dataset):
    vacancies = dataset
    vacancies_len = len(vacancies)
    progress_bar = IncrementalBar('Vacancies geocoded:',
                                  max=int(vacancies_len))
    for vacancy in vacancies:
        if 'location' not in vacancy:
            continue
        if isinstance(vacancy['location'], (list, tuple)):
            location_codes = set()

            for location in vacancy['location']:
                location_codes.add(get_region_by_forward_geocoding(location))
            vacancy['location'] = location_codes
        else:
            vacancy['location'] = get_region_by_forward_geocoding(vacancy['location'])
        progress_bar.next()
    progress_bar.finish()
    return vacancies


def geocoding_on_files(directory_path: str, upload_path: str):
    vacancies = start_geocoding(read_directory(directory_path))
    create_json(vacancies, upload_path, 'geocoded')

