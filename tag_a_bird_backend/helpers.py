from os import getenv
import requests
from json import loads
from .models import Record
from .db import db_session

def populate_db_from_coreo(db_session, country: str) -> str:
    """Populates the database with the last 100 records from the coreo API"""

    limit = 100
    total_count = 0

    def coreo_request(limit) -> dict:
        api_url = "https://api.coreo.io/graphql"
        request_header = {
            "Authorization": getenv("COREO_API_KEY"),
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Connection": "Keep-Alive"
        }
        query = f"""
        {{
            records(where: {{
                projectId: 462,
                data: {{country: "{country}"}}
            }},
            limit: {limit},
            order: "createdAt") {{
                id
                data
            }}
        }}"""

        request_body = {"query": query}
        response = requests.post(api_url, headers=request_header, json=request_body)
        print('Request made')
        if response.status_code == 200:
            try:
                response_json = loads(response.text)
                return response_json
            except Exception as e:
                print(f"Error parsing response JSON: {e}")
                return {}
        else:
            print(f"Request failed with status code {response.status_code}")
            return {}

    count = 0
    response = coreo_request(limit=limit)
    
    if response and "data" in response and "records" in response["data"]:
        try:
            for record in response["data"]["records"]:
                if not db_session.query(Record).filter_by(id=record["id"]).first():
                    new_record = Record.from_json(json=record["data"], id=record["id"])
                    db_session.add(new_record)
                    count += 1
            db_session.commit()
            total_count += count
            print(f"Added {count} records to the database")
        except Exception as e:
            db_session.rollback()
            print(e)
            return f"Error: {e}"
    else:
        print("No records found or API request failed.")
    
    return f"Database populated with {total_count} records from {country}"