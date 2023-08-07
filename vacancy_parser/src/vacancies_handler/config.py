import os
from dotenv import load_dotenv

load_dotenv()

""" MapBox geocoder API token """
ACCESS_TOKEN = os.getenv('MapBox_Token')

""" MAIN DB connection data """
MAIN_DB_CON_DATA = os.getenv('Main_DB_Con')

""" Path to directory for saving parsed data """
PATH_TO_REPOSITORY = 'vacancy_parser/src/data_storage'

""" Basename for generated files """
BASENAME = "parsed_vacancies"

""" Number of allowable errors when parsing one page """
ERROR_LIMIT = 5

""" Delay multiplier for requests to the source (sec) """
DELAY_MULTIPLIER = 5

""" ML model file path for classification """
ML_MODEL_PATH = 'vacancy_parser/src/models/model_v1.pk'
