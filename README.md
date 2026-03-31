# 🎅 Secret Santa — Acme Corp

An automated, full-stack Secret Santa assignment system built with **Python (Flask) + React + MongoDB**.

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3, Flask-CORS |
| Algorithm | Pure Python shuffle-and-verify derangement |
| Database | MongoDB (via PyMongo) |
| Frontend | React 18, React Router 6, Axios |
| Export | CSV, XML (ElementTree), XLSX (openpyxl) |
| Tests | pytest 8, pytest-cov (37 tests) |
| Container | Docker, Docker Compose |

## Quick Start

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your MONGO_URI
python app.py          # → http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm start              # → http://localhost:3000
```

### Docker (all-in-one)
```bash
docker compose up --build
```

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Health check |
| POST | /api/assignments/generate | Generate assignments (CSV/XLSX upload) |
| GET | /api/assignments/{year} | Fetch saved assignments |
| GET | /api/assignments/years | List all saved years |

### POST /api/assignments/generate

**multipart/form-data fields:**
- `employees_file` *(required)* — CSV or XLSX
- `previous_file` *(optional)* — previous year CSV
- `year` *(optional)* — integer year (default: current)
- `format` *(optional)* — `json` | `csv` | `xml`

## Input Format

**Employee CSV:**
```csv
Employee_Name,Employee_EmailID
Alice Smith,alice@acme.com
Bob Jones,bob@acme.com
```

**Previous Assignments CSV:**
```csv
Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
Alice Smith,alice@acme.com,Bob Jones,bob@acme.com
```

## Running Tests
```bash
cd backend
pytest                                       # 37 tests
pytest --cov=src --cov-report=term-missing   # with coverage
```

## Assignment Algorithm

Shuffle-and-verify derangement with up to 1,000 retries:
1. Shuffle the receiver list
2. Pair each giver with the shuffled receiver
3. Reject pairs that break constraints (self-assign or prior-year repeat)
4. Retry on failure — raise `AssignmentError` after MAX_RETRIES

## Project Structure
```
secret-santa/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── data/               ← sample Employee-List.xlsx + previous CSV
│   ├── src/
│   │   ├── models/         ← Employee, Assignment dataclasses
│   │   ├── parsers/        ← CSV/XLSX file parsers
│   │   ├── validators/     ← input validation
│   │   ├── services/       ← assignment engine, CSV/XML export, MongoDB
│   │   ├── routes/         ← Flask REST API
│   │   └── config/         ← app factory
│   └── tests/              ← 37 pytest tests across 5 modules
├── frontend/
│   └── src/
│       ├── pages/          ← GeneratePage, HistoryPage
│       ├── components/     ← FileUpload, AssignmentTable, ExportButtons
│       └── services/       ← axios API client
├── docker-compose.yml
└── README.md
```

## Environment Variables
| Variable | Default | Description |
|---|---|---|
| FLASK_DEBUG | false | Enable debug mode |
| PORT | 5000 | Flask server port |
| MONGO_URI | (empty) | MongoDB URI (optional) |

*Built for the DigitalXC Secret Santa Coding Challenge*
