WorkFlow Pro - QA Automation Framework

This repository contains the QA automation solution for the "WorkFlow Pro" B2B SaaS platform.

Framework Design:

This framework is built using Python with Pytest and Playwright. It follows the Page Object Model (POM) to ensure the code is maintainable and scalable.

tests/: Contains all test scripts, organized by type (UI, API, E2E).
page_objects/: Intended for page-specific classes and locators.
utils/: Intended for reusable helper utilities like an API client.
config/: Stores environment-specific configuration files.
test_data/: Stores test data used as input for tests.
.env: Stores all secrets and credentials.

Prerequisites:

Python 3.8+
pip

Setup Instructions

Clone the repository:
git clone https://github.com/TheSpecialOne-1/Bynry_automation_Case_Study
cd workflowpro-automation

Install dependencies:
pip install -r requirements.txt

Install Playwright browsers:
playwright install

Configure your environment:
Create a file named .env in the project root.
Copy the contents of .env.example into it and fill in your actual credentials.

How to Run Tests

Run all tests:
pytest

Run only the UI tests:
pytest tests/ui/

Generate an HTML report:
pytest --html=reports/report.html

Test Reports:

Test execution reports are generated in the reports/ directory. Open report.html in a browser to view the detailed results with logs and statuses.
