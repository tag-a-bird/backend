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
        try:
            response = requests.post(api_url, headers=request_header, json=request_body)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Request failed: {e}"}
        except ValueError as e:
            return {"error": f"Error parsing response JSON: {e}"}

    try:
        response = coreo_request(limit=limit)
        if response and "data" in response and "records" in response["data"]:
            count = 0
            records = response["data"]["records"]
            if not records:
                return f"No records found or API request failed. { response }"
            for record in records:
                if not db_session.query(Record).filter_by(id=record["id"]).first():
                    new_record = Record.from_json(json=record["data"], id=record["id"])
                    db_session.add(new_record)
                    count += 1
            db_session.commit()
            total_count += count
        else:
            if "error" in response:
                return f"API request failed: {response['error']}"
            return "No records found or API request failed."
    except Exception as e:
        db_session.rollback()
        return f"Error: {e}"

    return f"Database populated with {total_count} records from {country}"