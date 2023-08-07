
"""Habr sources"""
habr_api = 'https://career.habr.com/api/v1/integrations/vacancies?access_token=your_token'


"""HeadHunter sources"""
__hh_devs_test = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
               '&professional_role=96&area=113&per_page=15&experience=noExperience&pages=10'

__hh_devs_no_exp = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
               '&professional_role=96&area=113&per_page=45&experience=noExperience'

__hh_devs_exp1_3_part = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
               '&professional_role=96&area=113&per_page=45&experience=between1And3' \
               '&schedule=shift&schedule=flexible&schedule=remote'

__hh_devs_exp1_3_full = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
                    '&professional_role=96&area=113&per_page=45&experience=between1And3' \
                    '&schedule=fullDay'

__hh_devs_exp3_6_part = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
                    '&professional_role=96&area=113&per_page=45&experience=between3And6' \
                    '&schedule=shift&schedule=flexible&schedule=remote'

__hh_devs_exp3_6_full = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
                    '&professional_role=96&area=113&per_page=45&experience=between3And6' \
                    '&schedule=fullDay'

__hh_devs_exp_6 = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
              '&professional_role=96&area=113&per_page=45&experience=moreThan6'


__hh_analytic_0_6 = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
                  '&professional_role=156&professional_role=10&professional_role=165' \
                  '&professional_role=150&professional_role=164&professional_role=148' \
                  '&area=113&per_page=45&experience=noExperience&experience=moreThan6&experience=between3And6'

__hh_analytic_1_3 = 'https://api.hh.ru/vacancies?enable_snippets=true&only_with_salary=true' \
                  '&professional_role=156&professional_role=10&professional_role=165&professional_role=150' \
                  '&professional_role=164&professional_role=148&area=113&per_page=45&experience=between1And3'

__hh_qa = 'https://api.hh.ru/vacancies?enable_snippets=true&per_page=45&only_with_salary=true&professional_role=124'

HH_URLS = (__hh_devs_no_exp, __hh_devs_exp1_3_part, __hh_devs_exp1_3_full, __hh_devs_exp3_6_part,
           __hh_devs_exp3_6_full, __hh_devs_exp_6, __hh_analytic_0_6, __hh_analytic_1_3, __hh_qa,)

HH_DEVS = (__hh_devs_no_exp, __hh_devs_exp1_3_part, __hh_devs_exp1_3_full,
            __hh_devs_exp3_6_part, __hh_devs_exp3_6_full, __hh_devs_exp_6,)

HH_ANALYTICS = (__hh_analytic_0_6, __hh_analytic_1_3,)

HH_QA =(__hh_qa,)