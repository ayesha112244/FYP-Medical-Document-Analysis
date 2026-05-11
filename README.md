# Medical Document Analysis System — FYP 2026

**University of Huddersfield | School of Computing and Engineering**  
**Student:** Ayesha Sohail | **ID:** U2386691  
**Module:** CHP2524-QGA-YEAR-2526 : Individual Project  
**Supervisor:** Alla Detinko | **Examiner:** Clay Palmeira  
**Submission Date:** 11 May 2026

---

## Project Overview

An end-to-end medical document analysis system that automatically extracts structured data from medical laboratory reports in PDF and image formats. The system uses OCR, NLP, and regex-based pattern matching to extract patient information and medical values, stores results in a MySQL database, and presents them through a Laravel web application.

---

## Repository Structure
FYP-Medical-Document-Analysis/
│
├── app/                        # Laravel controllers and models
│   ├── Http/Controllers/       # AuthController, ReportController, UploadController
│   └── Models/                 # User, Report, MedicalValue
│
├── database/migrations/        # MySQL table definitions
├── resources/views/            # Laravel Blade templates
├── routes/web.php              # Application routes
├── composer.json               # PHP dependencies
│
├── pipeline.py                 # Main extraction pipeline
├── api_server.py               # FastAPI REST API server
├── evaluate.py                 # Accuracy evaluation script
├── insert_to_db.py             # Dataset insertion script
└── patterns.py                 # Regex pattern library
---

## Key Technologies

| Layer | Technology |
|---|---|
| OCR Engine | Tesseract 5 via pytesseract |
| PDF Parsing | Apache Tika |
| NLP & Extraction | spaCy, Regular Expressions |
| API Server | FastAPI (Python) |
| Web Framework | Laravel 11 (PHP 8.2) |
| Database | MySQL via XAMPP |
| Frontend | Bootstrap 5, Laravel Blade |

---

## Evaluation Results

| Metric | Score |
|---|---|
| Overall Accuracy | 82.1% |
| Precision | 96.1% |
| Recall | 85.0% |
| F1 Score | 90.2% |

Evaluated across 50 test documents — Synthetic PDF, Online PDF, PNG Screenshots, JPEG Camera Photos.

---

## Setup Instructions

Full technical setup instructions are documented in **Appendix A** of the project report.

Quick start:
1. Install XAMPP, Python 3.10+, Tesseract OCR
2. Run `pip install -r requirements.txt`
3. Start FastAPI: `python -m uvicorn api_server:app --host 127.0.0.1 --port 8001`
4. Start Laravel: `php artisan serve`
5. Access at `http://127.0.0.1:8000`
