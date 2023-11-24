from os import getenv
import requests
from json import loads
from .models import Record
from .db import db_session

def populate_db_from_coreo(db_session, country: str) -> str:
    """Populates the database with records from the coreo API"""

    limit = 10
    offset = 0
    total_count = 0

    def coreo_request(limit, offset) -> dict:
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
        # print(f'this request sent > body:{response.request.body}, headers:{response.request.headers} 
        # this response came back > status_code:{response.status_code}, text:{response.text}')
        print('request made')
        try:
            response_json = loads(response.text)
            # print(f'{response_json}')
            return response_json
        except Exception as e:
            print(e)
            return {}

    # find the record in response that matches the last record in the database from the same country and add all records after that one to the database
    # if there are no records in the database from that country, add all records from that country to the database
    while True:
        response = coreo_request(limit=limit, offset=offset)
        records_to_add = response.get("data", {}).get("records", [])
        if not records_to_add:
            break  # No more records to process

        count = 0
        for record_data in records_to_add:
            try:
                # Check if the record already exists
                if not db_session.query(Record).filter_by(id=record_data['id']).first():
                    new_record = Record.from_json(json=record_data["data"], id=record_data["id"])
                    db_session.add(new_record)
                    count += 1
                else:
                    print(f"Record with id {record_data['id']} already exists. Skipping.")
            except Exception as e:
                db_session.rollback()
                print(f"Error: {e}")
                return f"Error: {e}"

        try:
            if count > 0:
                db_session.commit()  # Commit outside the loop to minimize database transactions
                print(f"Added {count} records to the database")
                total_count += count
        except IntegrityError as e:
            db_session.rollback()
            print(f"A record with this ID already exists. Error: {e}")
            continue  # Continue with the next batch of records

        offset += limit  # Increase the offset to fetch the next batch of records

    return f"Database populated with {total_count} records from {country}"
