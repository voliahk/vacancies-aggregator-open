class ApiManual:
    FIELD_NAMES = ['id', 'name', 'salary', 'date_publication',
                   'location', 'employment', 'remote', 'skills', 'description']

    def __init__(self, source_name, json_name, start_page, pages, id, name, salary, date_publication,
                 location=None, employment=None, remote=None, skills=None, description=None):
        self.source_name = source_name
        self.json_name = json_name
        self.start_page = start_page
        self.pages = pages
        self.id = id
        self.name = name
        self.salary = salary
        self.date_publication = date_publication
        self.location = location
        self.employment = employment
        self.remote = remote
        self.skills = skills
        self.description = description


HH_MANUAL = ApiManual('api.hh.ru', "items", 0, "pages",
                      "id", "name",
                      {"jsonKey": "salary",
                       "manual": {"salary_from": "from", "salary_to": "to", "currency": "currency"}},
                      "published_at",
                      {"jsonKey": "area", "manual": {"location": "name"}},
                      {"jsonUrl": "url", "manual": {"jsonKey": "employment", "manual": {"employment": "id"}}},
                      {"jsonUrl": "url", "manual": {"jsonKey": "schedule", "manual": {"remote": "id"}}},
                      {"jsonUrl": "url", "manual": {"jsonKey": "key_skills", "manual": {"skill": "name"}}},
                      {"jsonKey": "snippet", "manual": {"description": "requirement"}},
                      )

HABR_MANUAL = ApiManual('career.habr.com', "list", 0, {"jsonKey": "meta", "manual": {"pages": "totalPages"}},
                            "id", "title",
                            {"jsonKey": "salary",
                             "manual": {"salary_from": "from", "salary_to": "to", "currency": "currency"}},
                            {"jsonKey": "publishedDate", "manual": {"date_publication": "date"}},
                            {"jsonKey": "locations", "manual": {"location": "title"}},
                            "employment",
                            "remoteWork",
                            {"jsonKey": "skills", "manual": {"skill": "title"}},
                            )
