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

Requires Python 3.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Terminal 1, the API:

```bash
python app.py
```

Terminal 2, the web page:

```bash
cd frontend
python -m http.server 5500
```

Open http://127.0.0.1:5500 in your browser.
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

## Who could use this tool (Kenya)

The tool logs a number per place or person each day and shows a running
total. Any small business that records daily figures and adds them up
by hand can use the same pattern:

| Business type | What they log daily |
|---|---|
| Poultry and egg farmers | Eggs per shed |
| Dairy farmers and milk collection groups | Litres per cow or farmer |
| Small shops and kiosks | Daily sales and stock counts |
| Salons and barbershops | Customers served and takings |
| Boda boda and matatu owners | Daily collection per vehicle |
| Fish farmers | Fish harvested per pond |
| School canteens and eateries | Meals sold and takings |

## Price points (estimates, to be confirmed with local market research)

| Tier | Includes | One-time (KES) | Monthly (KES) |
|---|---|---|---|
| Basic | API and web page deployed online, one business, training | 15,000 to 25,000 | 1,500 to 3,000 |
| Standard | Basic plus database, login, totals per shed or per week | 35,000 to 60,000 | 3,000 to 6,000 |

How I arrived at these: estimated hours multiplied by an hourly rate,
plus the monthly hosting cost and support time. Larger operations with
several sites pay more because accurate totals are worth more to them.

The current version is a prototype with in-memory storage and no login.
A database and login are required before it is client-ready.

## Pricing (to build, deploy and maintain for a poultry farmer)

**One-time build and deployment: UGX 000,000**
Includes: custom API for the farmer's sheds, deployment online,
setup, testing, and a short training session.

**Monthly maintenance: UGX 600,000 per month**
Includes: hosting, backups, bug fixes, and support by phone or WhatsApp.