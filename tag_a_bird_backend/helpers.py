from os import getenv
import requests
from json import loads
from .models import Record
from .db import db_session

def populate_db_from_coreo(db_session, country: str) -> str:
    """Populates the database with records from the coreo API"""

    limit = 100
    offset = 0
    total_count = 0

    def coreo_request(limit, offset) -> dict:
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
            offset: {offset},
            order: "createdAt") {{
                id
                state
                lat
                lng
                createdAt
                updatedAt
                deletedAt
                updatedAtPrecise
                commentsCount
                title
                description
                associatesCount
                liked
                likesCount
                deleted
                requestId
                anonymous
                data
                verificationState
                verified
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

    if db_session.query(Record).filter_by(country=country).first() is None:
        count = 0
        response = coreo_request(limit=limit, offset=offset)
        
        while response and "data" in response and "records" in response["data"] and len(response["data"]["records"]) == limit:
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
            offset += count
            total_count += count
            count = 0
            response = coreo_request(limit=limit, offset=offset)
            
        if response and "data" in response and "records" in response["data"]:
            try:
                for record in response["data"]["records"]:
                    new_record = Record.from_json(json=record["data"], id=record["id"])
                    db_session.add(new_record)
                    count += 1
                db_session.commit()
                print(f"Added {count} records to the database")
                total_count += count
            except Exception as e:
                db_session.rollback()
                print(e)
                return f"Error: {e}"
    else:
        db_last_record = db_session.query(Record).filter_by(country=country).order_by(Record.created_at.desc()).first()
        count = 0
        response = coreo_request(limit=limit, offset=offset)
        
        while response and "data" in response and "records" in response["data"] and len(response["data"]["records"]) == limit:
            try:
                for record in response["data"]["records"]:
                    if record["id"] == db_last_record.id:
                        break
                    new_record = Record.from_json(json=record["data"], id=record["id"])
                    db_session.add(new_record)
                    count += 1
            except Exception as e:
                db_session.rollback()
                count = 0
                print(e)
                return f"Error: {e}"
            db_session.commit()
            offset += count
            total_count += count
            count = 0
            response = coreo_request(limit=limit, offset=offset)
            
    return f"Database populated with {total_count} records from {country}"