# WebTrust

# Overview

A browser extension, web application, and desktop application that evaluates the trustworthiness of websites using public cybersecurity data, website security features, and a custom trust scoring algorithm.

# Technologies and Skills

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Requests
- National Vulnerability Database (NVD) API

## Frontend

- React
- JavaScript
- HTML
- CSS
- Vite

## Browser Extension

- Chrome Extensions (Manifest V3)
- Declarative Net Request API
- Chrome Tabs API

## Database

- PostgreSQL (AWS RDS)

# Installation

## Prerequisites

- Python 3.14+
- Node.js
- PostgreSQL
- Google Chrome

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Database Setup

Link AWS database to PostgreSQL and configure:

```
DATABASE_URL=
```

Run migrations:

```bash
alembic upgrade head
```

## Chrome Extension Setup

1. Open Chrome

2. Navigate to

```
chrome://extensions
```

3. Enable Developer Mode

4. Click

```
Load unpacked
```

5. Select the extension folder.


# Data Flow

(The flow's direction is from top to bottom.)
```
                             NVD
                              │
                Desktop Application Data Collector
                              │
                          Database
                              │
                    Trust Score Calculation
                              │
                           REST API
                              │
                        Chrome Extension
                              │
                        Site Block / Allow
```

# Features

- Company database
- Relative trust score ranking
- Automatic NVD synchronisation
- Security header detection
- Security posture scanning
- Automatic webpage blocking
- AWS-hosted PostgreSQL database