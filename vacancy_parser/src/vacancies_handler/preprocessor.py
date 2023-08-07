from config import BASENAME
from geocoder import start_geocoding
from tech_checker import start_search
from classifier import dataset_prediction

import json
import regex as re
import datetime


class Preprocessor:
    immutable_data = ["source", "date_publication"]
    employment = {'career.habr.com': {'full_time': 'full', 'part_time': 'part'},
                  'api.hh.ru': {'full': 'full', 'part': 'part', 'project': 'part', 'volunteer': 'part',
                                'probation': 'probation'}}
    remote = {'api.hh.ru': 'remote'}

    def __standardize_values(self, processed_data):
        dataset_length = len(processed_data)

        for i in range(dataset_length):
            source_name = processed_data[i]['source']
            if source_name in self.employment:
                for key, item in self.employment[source_name].items():
                    if processed_data[i]['employment'] == key:
                        processed_data[i]['employment'] = item

            if source_name in self.remote:
                if processed_data[i]['remote'] == self.remote[source_name]:
                    processed_data[i]['remote'] = True
                else:
                    processed_data[i]['remote'] = False

    def __clear_string(self, processed_data):
        regular = r'[^\p{L}\p{N}\p{Space}+#]|[\n\r]'
        for row in processed_data:
            for key, value in row.items():

                if key in self.immutable_data:
                    continue
                if not isinstance(value, (str, list)):
                    continue

                if isinstance(value, list):
                    row[key] = [re.sub(regular, '', item.replace('-', ' ').replace('/', ' ')).lower().replace('ё', 'е')
                                for item in value]
                else:
                    row[key] = re.sub(regular, '', value.replace('-', ' ').replace('/', ' ')).lower().replace('ё', 'е')

    @staticmethod
    def __create_json(processed_data, upload_path):
        def generate_filename():
            suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            generated_name = "_".join([BASENAME, suffix]) + '.json'
            return generated_name

        filename = generate_filename()
        with open(upload_path + '/' + filename, 'w', encoding='utf-16') as json_file:
            json.dump(processed_data, json_file, ensure_ascii=False)

    def process_data(self, dataset, upload_path: str):
        processed_data = dataset
        self.__standardize_values(processed_data)
        self.__clear_string(processed_data)
        # TODO Переделать
        processed_data = start_geocoding(processed_data)
        processed_data = start_search(processed_data)
        processed_data = dataset_prediction(processed_data)
        self.__create_json(processed_data, upload_path)