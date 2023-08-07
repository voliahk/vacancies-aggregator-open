from config import MAIN_DB_CON_DATA
from support_func_json import read_directory

from progress.bar import IncrementalBar
from psycopg2 import OperationalError

import psycopg2
import time
import ast


QUERY = "INSERT INTO vacancies(" \
        "id_source, id_area, id_employment, " \
        "original_id, title, salary_from, " \
        "salary_to, currency, remote, date_publication) " \
        "VALUES (%(source)s, %(id_area)s, %(id_employment)s, %(id)s, %(title)s, " \
        "%(salary_from)s, %(salary_to)s, %(currency)s, %(remote)s, %(date_publication)s) RETURNING id_vacancy;"

SUB_TABLES = {'vacancy_subject': 'location', 'vacancy_technology': 'skill'}


def get_connection():
    try:
        time.sleep(0.100)
        return psycopg2.connect(**ast.literal_eval(MAIN_DB_CON_DATA))
    except OperationalError as e:
        print(e)


def get_reference_table(req_table: str, conn):
    reference_data = None

    try:
        cursor = conn.cursor()
        if req_table == 'employment':
            cursor.execute('SELECT title, id_employment FROM employment')
            reference_data = cursor.fetchall()
        elif req_table == 'vacancies_source':
            cursor.execute('SELECT title, id_source FROM vacancies_source')
            reference_data = cursor.fetchall()
        elif req_table == 'professional_area':
            cursor.execute('SELECT title, id_area FROM professional_area')
            reference_data = cursor.fetchall()
        elif req_table == 'subject':
            cursor.execute('SELECT iso_code, id_subject FROM subject')
            reference_data = cursor.fetchall()

        cursor.close()
    except Exception as e:
        conn.rollback()
        print(e)

    if reference_data:
        return dict(reference_data)
    return reference_data


def insert_into_db(query_params: dict, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(QUERY, query_params)
        db_id_vacancy = cursor.fetchone()
        cursor.close()
        return db_id_vacancy
    except Exception as e:
        print(e)


def handle_vacancies(vacancies: (list, tuple)):
    def numeric_preparation(value):
        # TODO Перенести в препроцессор
        if value.isnumeric():
            return int(value)
        return None

    def constants_preparation(value):
        # TODO Перенести в препроцессор
        if value == 'none':
            return None
        elif value == 'true':
            return True
        elif value == 'false':
            return False
        return value


    conn = get_connection()
    if not conn:
        return None

    employment_table = get_reference_table('employment', conn)
    area_table = get_reference_table('professional_area', conn)
    source_table = get_reference_table('vacancies_source', conn)
    subject_table = get_reference_table('subject', conn)

    if any([employment_table, area_table, source_table, subject_table]) is None:
        conn.close()
        return None

    progress_bar = IncrementalBar('Vacancies loaded in db',
                                  max=int(len(vacancies)))
    for vacancy in vacancies:
        query_params = dict()
        query_params['source'] = source_table[vacancy['source']]
        query_params['id_area'] = area_table[vacancy['class']]
        query_params['id_employment'] = employment_table[vacancy['employment']]
        query_params['id'] = vacancy['id']
        query_params['title'] = vacancy['name']
        query_params['salary_from'] = numeric_preparation(vacancy['salary_from'])
        query_params['salary_to'] = numeric_preparation(vacancy['salary_to'])
        query_params['currency'] = constants_preparation(vacancy['currency'])
        query_params['remote'] = constants_preparation(vacancy['remote'])
        query_params['date_publication'] = vacancy['date_publication']

        time.sleep(0.10)
        db_id_vacancy = insert_into_db(query_params, conn)
        if db_id_vacancy:
            if load_sub_table(db_id_vacancy, vacancy, subject_table, conn):
                conn.commit()
            else:
                conn.rollback()
        else:
            conn.rollback()

        progress_bar.next()
    progress_bar.finish()
    conn.close()


def load_sub_table(id_vacancy, vacancy, subject_table, conn):
    def return_list(value):
        if isinstance(value, str):
            return [value]
        return value

    def get_id_subject(subject_table, iso_code: str):
        return subject_table[iso_code]

    for sub_table_name, sub_table_key in SUB_TABLES.items():

        params = list()
        values = return_list(vacancy[sub_table_key])
        count_elmts = len(values)
        if count_elmts < 1:
            continue

        for value in values:
            params.append(id_vacancy)
            if sub_table_name == 'vacancy_subject':
                params.append(get_id_subject(subject_table, value))
            else:
                params.append(value)

        query = "INSERT INTO"
        if sub_table_name == 'vacancy_subject':
            query += " vacancy_subject(id_vacancy, id_subject) VALUES (%s, %s)"
        elif sub_table_name == 'vacancy_technology':
            query += " vacancy_technology(id_vacancy, id_technology) VALUES (%s, %s)"
        for _ in range(1, count_elmts):
            query += ", (%s, %s)"
        else:
            query += ';'

        try:

            cursor = conn.cursor()
            cursor.execute(query, params)
            cursor.close()
        except Exception as e:
            print(e)
            return False
    return True


def upload_to_db_on_file(directory_path: str):
    vacancies = read_directory(directory_path)
    handle_vacancies(vacancies)
