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
                data:{{country: {country}, species: {
        'ne': 'null'
    }}}
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
    if db_session.query(Record).filter_by(country=country).first() is None:
        count = 0
        response = coreo_request(limit=limit, offset=offset)
        
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
            # print(f"Added {count} records to the database")
            offset += count
            # print(offset)
            total_count += count
            count = 0
            response = coreo_request(limit=limit, offset=offset)
            
        try:
            for record in response["data"]["records"]:
                new_record = Record.from_json(json=record["data"], id=record["id"])
                db_session.add(new_record)
                count += 1
            db_session.commit()
            print(f"Added {count} records to the database")
            total_count += count
            count = 0
        except Exception as e:
            db_session.rollback()
            count = 0
            print(e)
            return f"Error: {e}"   
        
    else:
        db_last_record = db_session.query(Record).filter_by(country=country).order_by(Record.created_at.desc()).first()
        count = 0
        # print(f'there are already some records from {country}')
        print(limit, offset)
        response = coreo_request(limit=limit, offset=offset)
        
        while len(response["data"]["records"]) == limit:
            try:
                for record in response["data"]["records"]:
                    if record["id"] == db_last_record.id:
                        break
                    new_record =Record.from_json(json=record["data"], id=record["id"])
                    db_session.add(new_record)
                    count += 1
            except Exception as e:
                db_session.rollback()
                count = 0
                print(e)
                return f"Error: {e}"
            db_session.commit()
            print(f"Added {count} records to the database")
            offset += count
            # print(offset)
            total_count += count
            count = 0
            response = coreo_request(limit=limit, offset=offset)
            
    return f"Database populated with {total_count} records from {country}"
