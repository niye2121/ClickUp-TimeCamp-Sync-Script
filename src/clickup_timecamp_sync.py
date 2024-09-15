import http.client
import json
import urllib.parse
import datetime
import time


def convert_date_to_unix_millis(date_str):
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return int(time.mktime(dt.timetuple()) * 1000)  # Convert to milliseconds

# ClickUp API: Fetch Time Entries for a Specific Assignee with Date Range
def get_clickup_time_entries(clickup_api_key, team_id, assignee_id, list_id, start_date, end_date):
    url = f"/api/v2/team/{team_id}/time_entries"
    
    start_date_millis = convert_date_to_unix_millis(start_date)
    end_date_millis = convert_date_to_unix_millis(end_date)

    query = {
        "assignee": assignee_id,
        "list_id": list_id,
        "start_date": start_date_millis,
        "end_date": end_date_millis
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": clickup_api_key
    }
    
    conn = http.client.HTTPSConnection("api.clickup.com")
    encoded_query = urllib.parse.urlencode(query)
    conn.request("GET", f"{url}?{encoded_query}", headers=headers)
    
    response = conn.getresponse()
    data = response.read().decode('utf-8')

    conn.close()

    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return []

    return parsed_data.get('data', [])

# TimeCamp API: Fetch existing entries for a specific date range
def get_existing_time_entries(timecamp_api_key, start_date, end_date):
    conn = http.client.HTTPSConnection("app.timecamp.com")
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {timecamp_api_key}',
        'Content-Type': 'application/json'
    }

    url = f"/third_party/api/entries?from={start_date}&to={end_date}"
    conn.request("GET", url, headers=headers)

    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()

    if response.status == 200:
        return json.loads(data)
    else:
        print(f"Error fetching time entries from TimeCamp: {response.status} - {data}")
        return []

# Check if time entry exists in TimeCamp
def time_entry_exists(existing_entries, task_id):
    for entry in existing_entries:
        entry_description = entry.get('description', '')
        if task_id in entry_description:
            return True
    return False

# Create Time Entry in TimeCamp if not exists
def create_time_entry_if_not_exists(timecamp_api_key, description, start, end, duration, tags, task_id):
    start_date = start.split(" ")[0]  
    end_date = end.split(" ")[0]      
    
    existing_entries = get_existing_time_entries(timecamp_api_key, start_date, end_date)

    if time_entry_exists(existing_entries, task_id):
        print(f"====Time entry for '{description}' already exists in TimeCamp. Skipping creation.")
    else:
        create_timecamp_time_entry(description, start, end, duration, tags, timecamp_api_key, task_id)

# TimeCamp API: Create Time Entry
def create_timecamp_time_entry(description, start, end, duration, tags, timecamp_api_key, task_id):
    conn = http.client.HTTPSConnection("app.timecamp.com")
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {timecamp_api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "get_entries": 0,
        "date": start.split(" ")[0],
        "start": start,
        "start_time": start,
        "end": end,
        "end_time": end,
        "duration": duration,
        "tags": tags,
        "description": f"{description}-{task_id}"
    }

    json_data = json.dumps(data)
    conn.request("POST", "/third_party/api/entries", body=json_data, headers=headers)

    response = conn.getresponse()
    response_data = response.read().decode('utf-8')

    if response.status == 201:
        print(f"Time entry '{description}' successfully created in TimeCamp.")
    else:
        print(f"Error creating time entry in TimeCamp: {response.status} - {response_data}")

    conn.close()

# Sync time entries from ClickUp to TimeCamp
def sync_time_entries(clickup_api_key, timecamp_api_key, team_id, assignee_id, list_id, start_date, end_date):
    clickup_entries = get_clickup_time_entries(clickup_api_key, team_id, assignee_id, list_id, start_date, end_date)
    
    if not clickup_entries:
        print("No time entries to sync.")
        return
    
    for entry in clickup_entries:
        description = entry.get('description', '') or f"{entry['task']['id']}/{entry['task']['name']}"
        task_id = entry['id']
        duration = int(entry['duration']) // 1000 if 'duration' in entry else 0
        start_time = int(entry['start']) // 1000 if 'start' in entry else None
        end_time = int(entry['end']) // 1000 if 'end' in entry else None

        if not start_time or not end_time:
            print(f"Invalid start or end time for task: {description}")
            continue

        start = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

        tags = [{"tagId": tag['name']} for tag in entry.get('task', {}).get('tags', [])]

        create_time_entry_if_not_exists(timecamp_api_key, description, start, end, duration, tags, task_id)

# Example usage
def main():
    # Get inputs from user
    clickup_api_key = input("Enter your ClickUp API key: ")
    timecamp_api_key = input("Enter your TimeCamp API key: ")
    team_id = input("Enter your ClickUp Team ID: ")
    assignee_id = input("Enter the Assignee ID: ")
    list_id = input("Enter the List ID: ")
    start_date = input("Enter the Start Date (YYYY-MM-DD): ")
    end_date = input("Enter the End Date (YYYY-MM-DD): ")
   

    sync_time_entries(clickup_api_key, timecamp_api_key, team_id, assignee_id, list_id, start_date, end_date)

if __name__ == "__main__":
    main()

    