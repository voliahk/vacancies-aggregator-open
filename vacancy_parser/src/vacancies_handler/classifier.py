from config import ML_MODEL_PATH
from support_func_json import read_directory, create_json

from progress.bar import IncrementalBar

import dill
import time


def get_classifier_model(model_path: str):
    with open(model_path, 'rb') as model_file:
        loaded_model = dill.load(model_file)
        return loaded_model


def dataset_prediction(dataset: (list, tuple)):
    vacancies = dataset
    vacancies_len = len(vacancies)
    model = get_classifier_model(ML_MODEL_PATH)

    progress_bar = IncrementalBar('Vacancies classified:',
                                  max=int(vacancies_len))

    for i in range(vacancies_len):
        if 'name' in vacancies[i]:
            time.sleep(0.100)
            if any(model.predict_proba([vacancies[i]['name']])[0]) >= 0.4:  # TODO переделать
                vacancies[i].update({'class': model.predict([vacancies[i]['name']])[0]})
            else:
                vacancies[i].update({'class': 'none'})
        progress_bar.next()
    progress_bar.finish()
    return vacancies


def get_single_prediction(query: str):
    model = get_classifier_model(ML_MODEL_PATH)
    for probation in model.predict_proba([query])[0]:
        if probation >= 0.4:
            return model.predict([query])[0]


def classification_on_files(directory_path: str, upload_path: str):
    vacancies = dataset_prediction(read_directory(directory_path))
    create_json(vacancies, upload_path, 'classified')
