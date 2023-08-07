from json_parser import JsonParser
from preprocessor import Preprocessor
from config import PATH_TO_REPOSITORY

from api_manual import ApiManual,  HH_MANUAL, HABR_MANUAL
from sources import __hh_devs_test, HH_DEVS, HH_ANALYTICS, HH_QA


def handle_sources(sources: tuple, manual: ApiManual):
    parser = JsonParser()
    preproc = Preprocessor()
    for source in sources:
        parsed_data = parser.handle_source(manual, source)
        preproc.process_data(parsed_data, PATH_TO_REPOSITORY)


if __name__ == "__main__":
    handle_sources(__hh_devs_test, HH_MANUAL)
    # handle_sources(HH_DEVS, HH_MANUAL)
    # handle_sources(HH_ANALYTICS, HH_MANUAL)
    # handle_sources(HH_QA, HH_MANUAL)
    pass
