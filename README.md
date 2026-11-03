# Egg Production Tracker API

A simple REST API that lets a poultry farmer log daily egg production
per shed and see all records with a running total, replacing manual
WhatsApp tallying.

## Endpoints

| Method | URL | Purpose |
|---|---|---|
| POST | /api/eggs | Log a daily record |
| GET | /api/eggs | Return all records and the total |

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The server runs at http://127.0.0.1:5000

## Example: log a record

```bash
curl.exe -X POST http://127.0.0.1:5000/api/eggs -H "Content-Type: application/json" -d "@examples/record1.json"
```

Request body:

```json
{"shed": "Shed A", "date": "2026-11-02", "count": 120}
```

Response (201 Created):

```json
{"message": "Record saved", "record": {"shed": "Shed A", "date": "2026-11-02", "count": 120}}
```

## Example: get all records

```bash
curl.exe http://127.0.0.1:5000/api/eggs
```

Response (200 OK):

```json
{"record_count": 4, "records": [...], "total_eggs": 425}
```

## Validation

Returns 400 with an error message if the body is not JSON, a field
is missing, count is not a whole number of 0 or more, or the date
is not in YYYY-MM-DD format.

## Limitations

Data is stored in memory and is lost when the server restarts.
A database is the next step.

## Pricing (to build, deploy and maintain for a poultry farmer)

**One-time build and deployment: UGX 000,000**
Includes: custom API for the farmer's sheds, deployment online,
setup, testing, and a short training session.

**Monthly maintenance: UGX 600,000 per month**
Includes: hosting, backups, bug fixes, and support by phone or WhatsApp.