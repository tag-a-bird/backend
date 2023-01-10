from os import getenv
import requests
from json import loads
from .models import Record
from flask import flash

'''
TODO: 
- find and clean more dead code
- restructure graphql query
- handle inaccurate/vague exceptions
- shorten long parameter list
- rename functions
- remove more duplicate code
...
'''

def coreo_request(limit, offset, country) -> dict:
    api_url: str = "https://api.coreo.io/graphql"
    request_header: dict = {"Authorization": getenv("COREO_API_KEY"), "Content-Type": "application/json", "Accept": "*/*", "Connection": "Keep-Alive"}
    query = f"""{{
        records(where:{{
            projectId: 462,
            data:{{country: {country}}}
            }},
            limit:{limit},
            offset:{offset},
            order:"createdAt")
            {{
                id
                data
            }}
            }}"""

    request_body: dict = {"query": query}
    response = requests.post(api_url, headers=request_header, json=request_body)

    try:
        response_json = loads(response.text)
        # print(f'{response_json}')
        return response_json
    except Exception as e:
        print(e)
        return {}

def load_all_records(limit, offset, country, db_session):
    total_count = 0

    print(f"There was no record from {country} till now")
    count = 0
    response = coreo_request(limit=limit, offset=offset, country=country)

    while len(response["data"]["records"]) == limit:
        try:
            for record in response["data"]["records"]:
                new_record = Record.from_json(json=record["data"], id=record["id"])
                db_session.add(new_record)
                count += 1
        except Exception as e:
            db_session.rollback()
            count = 0
            print(e)
            return f"Error: {e}"
        db_session.commit()
        print(f"Added {count} more records to the database...")
        offset += count
        total_count += count
        count = 0
        response = coreo_request(limit=limit, offset=offset, country=country)
    
    flash("Database populated successfully")
    print(f"Database populated with {total_count} records from {country}")

def load_new_records_only(limit, offset, country, db_session):
    total_count = 0

    db_last_record = db_session.query(Record).filter_by(country=country).order_by(Record.created_at.desc()).first()
    count = 0
    checked = 0
    print(f'there are already some records from {country}')
    # print(f'last record\'s id is {db_last_record.id}')
    response = coreo_request(offset=offset, limit=limit, country=country)
    print(len(response["data"]["records"]))
    while len(response["data"]["records"]) == limit:
        try:
            for record in response["data"]["records"]:
                # if record["id"] == db_last_record.id:
                #     flash(f'There are no new records from {country}')
                #     print(f'There are no new records from {country}')
                #     return
                # else:
                    cheked_id = record["id"]
                    existing_id = db_session.query(Record).filter_by(id=cheked_id).first()
                    if not existing_id:
                        print('Adding new records to the database...')
                        new_record = Record.from_json(json=record["data"], id=record["id"])
                        db_session.add(new_record)
                        count += 1
                        checked += 1
                    else:
                        checked += 1
                        print('this already exist..')
        except Exception as e:
            db_session.rollback()
            count = 0
            print(e)
            return f"Error: {e}"
        db_session.commit()
        # print(f"Added {count} new records to the database")
        offset += checked
        total_count += count
        count = 0
        response = coreo_request(offset=offset, limit=limit, country=country)
    flash("Database updated successfully")
    print(f"Database populated with {total_count} records from {country}")


def populate_db_from_coreo(db_session, country: str) -> str:
    """Populates the database with records from the coreo API"""

    limit = 10
    offset = 0

    # find the record in response that matches the last record in the database from the same country and add all records after that one to the database
    # if there are no records in the database from that country, add all records from that country to the database
    if db_session.query(Record).filter_by(country=country).first() is None:
        load_all_records(limit, offset, country, db_session)
        
    else:
        load_new_records_only(limit, offset, country, db_session)
            