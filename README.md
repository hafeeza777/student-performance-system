Student Performance Analysis and Evaluation System
A full-stack web application built with Flask that automates student academic evaluation — calculating results, visualizing performance, generating certificates, and giving teachers a dashboard to monitor students, all in one place.
🔗 Live Demo: https://student-performance-system-1akk.onrender.com
What it does
Students log in, enter their subject marks, and instantly get their total, percentage, and pass/fail status calculated automatically.
Results are shown on an interactive dashboard with bar, pie, and line charts (Chart.js) so students can visualize their performance at a glance.
Students who pass can download a PDF certificate (generated with ReportLab) with their name, register number, percentage, and issue date.
Students who don't meet the pass criteria (40+ in every subject) are shown curated learning resources instead.
Teachers get a separate login and dashboard to view all student records, pass/fail counts, and top performers — no manual tracking needed.
Tech Stack
Layer
Tech
Backend
Python, Flask
Frontend
HTML5, CSS3, JavaScript
Database
SQLite
Charts
Chart.js
PDF Generation
ReportLab
Deployment
Render
How it works
Student logs in → enters name, register number, and subject marks
Backend calculates total marks, percentage, highest/lowest scores, and pass/fail status
Results render on a dashboard with charts and a performance summary
Pass → certificate download available. Fail → redirected to learning resources
Teachers log in separately to view aggregate stats across all students
Run it locally
git clone https://github.com/hafeeza777/student-performance-system.git
cd student-performance-system
pip install -r requirements.txt
python app.py
Then open http://localhost:5000 in your browser.
Known limitations
SQLite is used for simplicity — fine for a small/demo scale, would move to PostgreSQL or MySQL for production.
Authentication is basic (no password encryption yet) — a planned improvement.
Currently supports a fixed number of subjects.
Planned improvements
Role-based authentication with encrypted passwords
Student self-registration
Export results to Excel/PDF
QR-code certificate verification
Migration to a production-grade database
