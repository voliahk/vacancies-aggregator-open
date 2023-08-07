from api_manual import ApiManual
from config import ERROR_LIMIT, DELAY_MULTIPLIER
from progress.bar import IncrementalBar

import json
import requests
import time


class JsonParser:
    extended_vacancy: dict

    @staticmethod
    def get_json(url):
        try:
            request = requests.get(url)
            request.encoding = 'utf-8'
            return json.loads(request.text)
        except requests.exceptions.RequestException as e:
            return None

    @staticmethod
    def __extract_nested_value(nested_collection, manual):
        extracted_value = dict()

        if nested_collection is None:
            return extracted_value

        for field, json_key in manual.items():
            if isinstance(nested_collection, list):
                extracted_value[field] = [str(item[json_key]) for item in nested_collection]
            else:
                extracted_value[field] = str(nested_collection[json_key])
        return extracted_value

    def __safe_get(self, json_collection, field_value):
        parsed_data = None

        if not isinstance(field_value, dict):
            parsed_data = str(json_collection[field_value])
        elif field_value.get("jsonKey"):
            parsed_data = self.__extract_nested_value(json_collection[field_value["jsonKey"]],
                                                      field_value["manual"])
        elif field_value.get("jsonUrl"):
            if not self.extended_vacancy:
                if not json_collection[field_value.get("jsonUrl")]:
                    return parsed_data
                time.sleep(1)
                self.extended_vacancy = self.get_json(json_collection[field_value["jsonUrl"]])

            extended_manual = field_value["manual"]
            if extended_manual["jsonKey"] in self.extended_vacancy:
                parsed_data = self.__extract_nested_value(
                    self.extended_vacancy[extended_manual["jsonKey"]],
                    extended_manual["manual"])

        return parsed_data

    def __get_total_pages(self, api_manual: ApiManual, json_data):
        try:
            if isinstance(api_manual.pages, dict):
                total_pages = self.__safe_get(json_data, getattr(api_manual, 'pages'))['pages']
            else:
                total_pages = json_data[api_manual.pages]
            return total_pages
        except KeyError as e:
            return None

    def __get_parsed_vacancies(self, api_manual: ApiManual, vacancies):
        for vacancy in vacancies[api_manual.json_name]:
            parsed_vacancy = dict()
            self.extended_vacancy = dict()
            parsed_vacancy['source'] = api_manual.source_name

            for field_name in api_manual.FIELD_NAMES:
                field_value = getattr(api_manual, field_name)
                if field_value is not None:
                    parsed_data = self.__safe_get(vacancy, field_value)
                    if isinstance(parsed_data, dict):
                        parsed_vacancy.update(parsed_data)
                    else:
                        parsed_vacancy.update({field_name: parsed_data})
                else:
                    parsed_vacancy.update({field_name: None})

            yield parsed_vacancy

    def handle_source(self, api_manual: ApiManual, api_url: str):
        parsed_vacancies = []

        vacancies = self.get_json(api_url)
        if vacancies is None:
            return None

        total_pages = self.__get_total_pages(api_manual, vacancies)
        if total_pages is None:
            return None

        progress_bar = IncrementalBar('Pages processed:',
                                      max=int(total_pages))
        for page in range(api_manual.start_page, int(total_pages)):
            updated_url = api_url + "&page={}".format(page)
            is_page_parsed = False
            count_error = 0

            while not is_page_parsed and count_error < ERROR_LIMIT:
                time.sleep(DELAY_MULTIPLIER + DELAY_MULTIPLIER * count_error)
                vacancies = self.get_json(updated_url)

                if vacancies is None or api_manual.json_name not in vacancies or len(vacancies[api_manual.json_name]) == 0:
                    count_error += 1
                    continue

                if not is_page_parsed:
                    for item in self.__get_parsed_vacancies(api_manual, vacancies):
                        parsed_vacancies.append(item)
                    self.extended_vacancy = dict()
                    is_page_parsed = True
            progress_bar.next()
        progress_bar.finish()
        return parsed_vacancies
