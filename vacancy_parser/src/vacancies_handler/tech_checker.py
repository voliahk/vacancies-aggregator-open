from config import MAIN_DB_CON_DATA
from support_func_json import read_directory, create_json

from progress.bar import IncrementalBar

import regex as re
import psycopg2
import time
import ast


def get_connection():
    try:
        time.sleep(0.10)
        return psycopg2.connect(**ast.literal_eval(MAIN_DB_CON_DATA))
    except Exception as e:
        print(e)


def db_search_tech(conn: psycopg2.connect, query_text: str):
    try:
        id_tech = None

        cursor = conn.cursor()
        cursor.execute("SELECT id_technology, similarity(title, %(text)s) AS sml FROM technology_dictionary "
                       "WHERE title %% %(text)s ORDER BY sml DESC LIMIT 1", {'text': query_text})
        response = cursor.fetchone()
        # TODO Забыл порог учитывать (sml)
        if response is not None:
            id_tech = response[0]
        cursor.close()

        return id_tech
    except Exception as e:
        print(e)


def replace_chars(str_value: str) -> str:
    # TODO Вынести в препроцессор
    spec_chars = {'c plusplus': '(c|с|си)(|\\s)[+]{1,2}',
                  'c sharp': '(c|с|си)(|\\s)[#]{1}'}

    for swap_value, re_manual in spec_chars.items():
        regular = r'' + re_manual + ''
        if re.search(regular, str_value):
            return re.sub(regular, swap_value, str_value)
    return str_value


def start_search(dataset):
    vacancies = dataset
    vacancies_len = len(dataset)
    progress_bar = IncrementalBar('Vacancies tech checked:',
                                  max=int(vacancies_len))
    for vacancy in vacancies:
        if 'skill' in vacancy and len(vacancy['skill']) > 0:
            tech_stack = set()

            conn = get_connection()
            if conn is None:
                print('No connection to the database')
                progress_bar.next()
                continue

            for tech in vacancy['skill']:
                parsed_tech = replace_chars(tech)
                retrieved_value = db_search_tech(conn, str(parsed_tech))
                if retrieved_value is not None:
                    tech_stack.add(retrieved_value)
            conn.close()
            vacancy['skill'] = list(tech_stack)

        progress_bar.next()
    progress_bar.finish()
    return vacancies


def tech_search_on_files(directory_path: str, upload_path: str):
    vacancies = start_search(read_directory(directory_path))
    create_json(vacancies, upload_path, 'tech_checked')

