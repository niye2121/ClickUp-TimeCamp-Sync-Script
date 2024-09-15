# ClickUp to TimeCamp Sync Script

![ClickUp to TimeCamp Sync](assets/thumbnail.png)

This Python script allows you to sync time entries from **ClickUp** to **TimeCamp**. It fetches time entries for a specific assignee from ClickUp based on a provided date range and checks if the corresponding time entry already exists in TimeCamp. If the time entry does not exist, it creates a new entry in TimeCamp.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Clone the Repository or Download the Script](#1-clone-the-repository-or-download-the-script)
  - [Run the Script and Provide API Keys and Parameters](#2-run-the-script-and-provide-api-keys-and-parameters)
  - [Output](#3-output)
- [Script Workflow](#script-workflow)
- [Functions](#functions)
- [License](#license)

## Prerequisites

- **Python 3.7+**: Make sure you have Python installed. You can download it from [Python's official website](https://www.python.org/downloads/).
  
- **API Keys**:
  - **ClickUp API Key**: You need a valid ClickUp API key. You can generate it from your [ClickUp API Settings](https://app.clickup.com/settings/apps).
  - **TimeCamp API Key**: You need a valid TimeCamp API key. You can generate it from your [TimeCamp Integration Settings](https://www.timecamp.com/third_party/api/).

- **Dependencies**: The script uses only the built-in libraries like `http.client`, `json`, `urllib.parse`, `datetime`, and `time`, so no external libraries are required.

## Usage

### 1. Clone the Repository or Download the Script
You can either clone the repository or copy the Python script into your local environment.

```bash
git clone https://github.com/yourusername/clickup-timecamp-sync.git
cd clickup-timecamp-sync
```

### 2. Run the Script and Provide API Keys and Parameters
You can run the script by executing the following command in your terminal:

```bash
python src/sync.py
```
The script will prompt you to enter the following parameters:

- **ClickUp API Key**: You need to enter your ClickUp API key.
- **TimeCamp API Key**: You need to enter your TimeCamp API key.
- **ClickUp Team ID**: The ID of your ClickUp team.
- **Assignee ID**: The ID of the assignee whose time entries you want to fetch from ClickUp.
- **List ID**: The ID of the ClickUp list that contains the tasks you want to sync.
- **Start Date**: The start date for the time range in the format `YYYY-MM-DD`.
- **End Date**: The end date for the time range in the format `YYYY-MM-DD`.

Here’s an example of the script prompts:

```bash
clickup_api_key = input("Enter your ClickUp API key: ")
timecamp_api_key = input("Enter your TimeCamp API key: ")
team_id = input("Enter your ClickUp Team ID: ")
assignee_id = input("Enter the Assignee ID: ")
list_id = input("Enter the List ID: ")
start_date = input("Enter the Start Date (YYYY-MM-DD): ")
end_date = input("Enter the End Date (YYYY-MM-DD): ")
```
### 3. Output
The script will print output to the terminal, including the creation of new time entries or skipping existing ones:

```bash
Time entry 'task-id/Task Name' successfully created in TimeCamp.
====Time entry for 'task-id/Task Name' already exists in TimeCamp. Skipping creation.
```
## Script Workflow

- **Fetch Time Entries from ClickUp**: The script retrieves time entries for a specific assignee in a given list and date range from ClickUp.
- **Check Time Entries in TimeCamp**: Before creating a new entry in TimeCamp, it checks if the entry already exists by comparing task details.
- **Create Time Entry in TimeCamp**: If no matching entry exists, a new entry is created in TimeCamp.

## Functions

- `convert_date_to_unix_millis(date_str)`: Converts date string (`YYYY-MM-DD`) to Unix timestamp in milliseconds.
- `get_clickup_time_entries(clickup_api_key, team_id, assignee_id, list_id, start_date, end_date)`: Fetches time entries from ClickUp based on the team, assignee, list, and date range.
- `get_existing_time_entries(timecamp_api_key, start_date, end_date)`: Retrieves existing time entries from TimeCamp for a specific date range.
- `time_entry_exists(existing_entries, task_id)`: Checks if a time entry already exists in TimeCamp based on the task ID.
- `create_time_entry_if_not_exists(timecamp_api_key, description, start, end, duration, tags, task_id)`: Creates a new time entry in TimeCamp if it doesn't already exist.
- `create_timecamp_time_entry(description, start, end, duration, tags, timecamp_api_key, task_id)`: Sends the POST request to TimeCamp to create a new time entry.
- `sync_time_entries(clickup_api_key, timecamp_api_key, team_id, assignee_id, list_id, start_date, end_date)`: Orchestrates the workflow to fetch entries from ClickUp and sync them with TimeCamp.

## License

This script is open-source and free to use under the MIT License. You are welcome to modify it as per your requirements.
