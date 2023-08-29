

query_1 = """
    This is a resume. Can you give me the name, phone, email, country, city, linkedin, github,
    top four recent working experiences order by recent dates includes companies, title, working dates with the correct format date (mm/Y),
    technical skills,
    language,
    and college name, major?
    Give the answer in json format. If not available, please put 'null'
    For example, {"name": <name>,
                "phone": <phone>,
                "email": <email>,
                "country": <country>,
                "city": <city>,
                "linkedin": <if available or null>,
                "github": <if available or null>,
                "skills": <list of technical skills>,
                "language": <list of languages>,
                "working_experiences": [
                    {"company": <company>,
                    "title": <title>,
                    "working_date": <03/2022 - 04/2-23> },
                    {"company": <company>,
                    "title": <title>,
                    "working_date": <12/2021 - 02/2022> }
                    ],
                "college": <college name>,
                "major": <major>
                }
"""