# KU-Exam-Notifier

# Description:

KU-Exam-Notifier is an automated notification system designed to keep user informed about exam commencement dates. This script scrapes a public-facing website twice daily to check for new announcements. When a new announcement is detected, it downloads the attached PDF file, analyzes it using Llama3 hosted on GORQ, and sends you an alert via Telegram or WhatsApp. 

Features:

    Automated Scraping: Checks the website for new exam announcements twice a day.
    PDF Download & Analysis: Downloads the attached PDF files and analyzes them using Llama3.
    Instant Notifications: Sends alerts directly to your Telegram or WhatsApp.
    Customizable Prompt: Uses a special prompt to analyze the PDF content.

Technologies Used:

    Python
    Llama3 on GORQ (for PDF analysis)
    Telegram Bot API
    WhatsApp API
