# Egg Production Tracker

A small web tool that lets a poultry farmer log daily egg production per shed and see every record with a running total, replacing manual WhatsApp tallying.

<!-- After you take a screenshot of the working page, save it as screenshot.png in the project folder and remove the arrows around the next line:
![Egg tracker page](screenshot.png)
-->

## Problem and solution

A poultry farmer in Kasese has three sheds. Each day he sends himself egg counts on WhatsApp, and every Saturday he adds them up by hand. This is slow, and one wrong number ruins the total.

This project replaces that routine:

- The farm manager opens a web page, types the shed name, the date and the egg count, and clicks **Submit**.
- The record is saved through a REST API built with Flask.
- The page immediately shows every record in a table with the updated total, **without reloading**.

## Features

- REST API with `POST /api/eggs` (log a record) and `GET /api/eggs` (all records plus total).
- Input validation with clear error messages and correct HTTP status codes (`200`, `201`, `400`).
- Browser interface in plain HTML and JavaScript using `fetch()`.
- CORS configured for named origins only (no open "allow everyone" setting).

## Tech stack

| Part | Tool |
|---|---|
| API | Python 3 and Flask |
| CORS | Flask-CORS |
| Front end | HTML, CSS, JavaScript (`fetch`) |
| Testing | `curl.exe` and the browser |
| Storage | In-memory Python list (prototype) |

## Project structure

```text
egg-tracker-api/
  app.py              Flask API (endpoints, validation, CORS)
  requirements.txt    Python libraries needed
  README.md           This file
  .gitignore          Files Git should skip (venv, caches)
  examples/           Sample JSON requests
    record1.json
    record2.json
    record3.json
    record4.json
  frontend/
    index.html        The browser page (form, table, total)
```

## Setup and run

Requires Python 3.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On Mac or Linux, activate with `source venv/bin/activate`.

You need two terminals, one for each server.

**Terminal 1: the API**

```bash
python app.py
```

It runs at `http://127.0.0.1:5000`.

**Terminal 2: the web page**

```bash
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` in your browser.

## API reference

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/health` | Check that the server is running |
| POST | `/api/eggs` | Log a daily record |
| GET | `/api/eggs` | Return all records with a running total |

### POST /api/eggs

Request body (JSON):

```json
{"shed": "Shed A", "date": "2026-11-02", "count": 120}
```

Success response, status `201 Created`:

```json
{
  "message": "Record saved",
  "record": {"shed": "Shed A", "date": "2026-11-02", "count": 120}
}
```

Example using the sample file (Windows PowerShell, `curl.exe`):

```bash
curl.exe -X POST http://127.0.0.1:5000/api/eggs -H "Content-Type: application/json" -d "@examples/record1.json"
```

### GET /api/eggs

```bash
curl.exe http://127.0.0.1:5000/api/eggs
```

Response, status `200 OK`, after the four sample records:

```json
{
  "record_count": 4,
  "records": [
    {"shed": "Shed A", "date": "2026-11-02", "count": 120},
    {"shed": "Shed B", "date": "2026-11-02", "count": 95},
    {"shed": "Shed A", "date": "2026-11-03", "count": 110},
    {"shed": "Shed B", "date": "2026-11-03", "count": 100}
  ],
  "total_eggs": 425
}
```

### Validation and errors

POST returns status `400` with a message in the form `{"error": "..."}` when:

| Problem | Error message |
|---|---|
| Body is not valid JSON | Request body must be valid JSON |
| `shed`, `date` or `count` is missing (a shed of only spaces counts as missing) | shed, date and count are all required |
| `count` is not a whole number, or is below 0 | count must be a whole number, 0 or more |
| `date` is not in `YYYY-MM-DD` format | date must look like 2026-11-02 |

## How to test

**With curl.** Send the four files in `examples/` with the POST command above, then run the GET. Check by hand: 120 + 95 + 110 + 100 = 425. The response should show `record_count` 4 and `total_eggs` 425.

**In the browser.** Open `http://127.0.0.1:5500` and submit these records one at a time:

| Shed | Date | Count | Total shown |
|---|---|---|---|
| Shed A | 2026-11-02 | 120 | 120 |
| Shed B | 2026-11-02 | 95 | 215 |
| Shed A | 2026-11-03 | 110 | 325 |
| Shed B | 2026-11-03 | 100 | 425 |

The table and total update after each submit without a page reload. Typing only spaces in the shed box should produce a red error message and no new row.

## CORS

The page runs on port 5500 and the API on port 5000. A browser treats these as different origins and blocks the page from reading the API's replies unless the API allows it. `app.py` allows only:

```python
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])
```

Naming specific origins is safer than allowing every website to call the API.

## Limitations (this is a prototype)

- Data is stored in memory and is lost when the server restarts.
- No login, so anyone who can reach the server can add data.
- Totals are overall, not yet per shed or per week.
- Records cannot be edited or deleted.
- CORS allows only `http://127.0.0.1:5500` and `http://localhost:5500`. These must be changed to the real site address when deployed.
- It runs only on the developer's computer until it is deployed.

## Roadmap to a client-ready version

1. A database (SQLite to start, PostgreSQL when needed) so data survives restarts.
2. Login, so only the farm's staff can log or read data.
3. Totals per shed and per week, which is the farmer's real Saturday need.
4. Edit and delete for mistakes, and export to CSV or Excel.
5. Deployment online with HTTPS and automatic backups.

## Who could use this tool (Kenya)

The tool logs a number per place or person each day and shows a running total. Any small business that records daily figures and adds them up by hand can use the same pattern. Only the field names change (`shed` becomes `vehicle`, `pond` or `cow`).

| Business type | What they log daily | Suggested tier |
|---|---|---|
| Poultry and egg farmers with several sheds | Eggs per shed | Standard |
| Dairy farmers and milk collection groups | Litres per cow or farmer | Standard |
| Fish farmers with several ponds | Fish harvested per pond | Standard |
| Boda boda and matatu owners with several vehicles | Daily collection per vehicle | Standard |
| School canteens and eateries | Meals sold and takings | Starter or Standard |
| Small shops and kiosks | Daily sales and stock counts | Starter |
| Salons and barbershops | Customers served and takings | Starter |
| Produce sellers and market traders | Sacks or crates sold per day | Starter |

These are my reasoning about how such businesses work, not market research. Before pitching, talk to one or two real owners and check that daily logging is a real problem for them.

## Pricing (in Kenya shillings, KES)

The prices below are for the **client-ready version** (database, login, deployment), not the current prototype. They are estimates based on the research below and should be rechecked before quoting a real client.

### Price list

| | Starter | Standard |
|---|---|---|
| Best for | One site, one or two users | Several sheds, ponds or vehicles, several users |
| Web page and API deployed online | Yes | Yes |
| Database (data survives restarts) | Yes | Yes |
| Login | One shared login | Separate logins for manager and staff |
| Totals per shed or per week | Overall total | Per shed, per week, and overall |
| Edit and delete records, export to CSV | No | Yes |
| Training session | 1 hour | 2 hours |
| Free support after launch | 30 days | 30 days |
| **One-time build and deployment** | **KES 40,000** | **KES 70,000** |
| **Monthly hosting and support** | **KES 3,500** | **KES 6,000** |

Extras such as a WhatsApp or SMS entry method, M-Pesa features, or a custom domain are quoted separately.

### Quote for the Kasese poultry farmer (original assignment)

Three sheds, weekly totals per shed, a manager and a helper entering data: **Standard tier**.

- **Build and deployment: KES 70,000** one time.
- **Monthly maintenance: KES 6,000** (hosting, backups, bug fixes, and support by phone or WhatsApp).

### How the prices were calculated

**Rate used:** KES 1,200 per hour. This sits just above the KES 1,000 per hour floor suggested for Kenyan freelance developers and below the KES 1,500 to 3,000 suggested for someone with a year of client experience, because I am still building my track record.

| Item | Working | Result |
|---|---|---|
| Starter build | 25 hours x KES 1,200 = KES 30,000, plus 30% buffer for scope changes = KES 39,000 | **KES 40,000** (rounded) |
| Standard build | 45 hours x KES 1,200 = KES 54,000, plus 30% buffer = KES 70,200 | **KES 70,000** (rounded) |
| Starter monthly | Hosting about KES 1,700 + 1 hour support (KES 1,200) = KES 2,900, plus 20% margin = KES 3,480 | **KES 3,500** |
| Standard monthly | Hosting about KES 2,500 + 2 hours support (KES 2,400) = KES 4,900, plus 20% margin = KES 5,880 | **KES 6,000** |

The hour counts are my own estimates of the work. The monthly fee is roughly 9% of the build price in both tiers, so the two prices stay in proportion.

### Research behind the numbers

| Input | What I found | Source |
|---|---|---|
| Hourly rates | Kenyan freelance developers charge from about KES 1,500 to 8,000 per hour depending on experience. Early-career JavaScript programmers average about KES 1,000 per hour. | mctaba.com, Payscale |
| Project prices for local clients | About KES 20,000 to 50,000 for a basic website and KES 80,000 to 250,000 for a custom web application. | mctaba.com |
| Scope buffer | Add about 30% to the base price for changes that always appear. | mctaba.com |
| Hosting | An always-on Render web service plus a small PostgreSQL database cost about US$13 per month (July 2026). At about KES 129 per US dollar, that is about KES 1,700. Render's free web tier goes idle after 15 minutes, so it is unsuitable for a client. | render.com |
| Exchange rate | About KES 129 per US dollar in mid-2026. Check the current rate before quoting. | wise.com and other converters |

The Standard build price is a little below the lower end of the "custom web application" range because the scope is small and focused on one job.

### Notes before quoting a real client

- Prices exclude any tax you owe on your income. Check your obligations before quoting.
- If the client pays in another currency, convert at the day's rate and state the rate in the quote.
- A client can reasonably ask for a pilot month first. Offer a discount on the build price in return for feedback.
- No income is guaranteed. Many small clients want to see a working demo before paying.

## Author

Egidio K Ham, HamTech Ltd.