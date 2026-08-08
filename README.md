# WebTrust

# Overview

A browser extension, web application, and desktop application that evaluates the trustworthiness of websites using public cybersecurity data, website security features, and a custom trust scoring algorithm.

# Trust Score System

Each company receives a security score based on the evaluation of their security posture -- National Vulnerability Database (NVD), security headers, and security.txt file status. 

To avoid having companies with a high amount of vulnerability reports always appearing as the least trustworthy a relative scoring algorithm is used. A rating is then associated with the company depending on their score -- excellent, good, fair, poor, or critical.

# Technologies and Skills

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Requests
- NVD API

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

1. Link AWS RDS database to PostgreSQL and configure:

```
DATABASE_URL=
```

2. Run migrations:

```bash
alembic upgrade head
```

## Chrome Extension Setup

3. Open Chrome

4. Navigate to

```
chrome://extensions
```

5. Enable Developer Mode

6. Click

```
Load unpacked
```

7. Select the extension folder.

## Desktop app Setup

8. From the WebTrust directory, initiate the app:

```bash
python -m desktop.main
```

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

# Browser Extension

The Chrome extension automatically:

- Detects the website being visited
- Queries the backend
- Retrieves the company's trust score
- Blocks websites marked as Critical
- Redirects users to an explanation page

# Blocked Page

When a website is blocked, users are shown:

- Company name
- Domain
- Trust score
- Rating
- Associated security reports
- Security recommendations

This allows users to understand why the site was blocked rather than simply receiving a warning.

# Desktop App

The desktop app allows the user to manually:

- Scan the NVD for new entries.
- Sync NVD entries with existing companies in its database.
- Allow the user to forcefully refresh the database.
- Gives the user information about the status of the API, date of the last scan, and an overview of the amount of companies currently in the database.

# API Endpoints

Example endpoints include:

```
GET /companies
```

```
GET /reports
```

```
POST /companies?name={name}&domain={domain}
```

```
POST /reports/{company_id}
```

# Challenges

Some of the main technical challenges during development included:

- Designing a balanced trust algorithm
- Implementing relative scoring
- Preventing false-positive CVE matches
- Automatically linking NVD reports to companies
- Building a Manifest V3 Chrome extension
- Managing browser redirects without creating loops
- Displaying report information efficiently
- Keeping frontend and backend synchronised


# Future Improvements

Potential future work includes:

- Machine learning-based trust scoring, interpreting patterns of security incidents to block certain companies.
- Report confidence scoring to indicate to the user how confident the program is that a given NVD entry is about a company.
- Better CVE relevance matching to ensure that each NVD is being matched to the correct company.
- User account system that shows the history of dangerous sites they have connected to.
- Power BI analytics dashboard.
- Historical trust score graphs.
- Scheduled background NVD entry scanning.
- Firefox and Edge support.
- Additional security signal collection by checking URLs and gauging whether it is a malicious link.

# Why This Project?

Modern users often rely on browser warnings that provide little context beyond "unsafe".

WebTrust explores how public cybersecurity data, website security features, and automated analysis can be combined into an explainable trust scoring system that helps users make more informed decisions while browsing.

The project demonstrates full-stack software engineering, browser extension development, cybersecurity principles, database design, REST API development, and data-driven decision making.
