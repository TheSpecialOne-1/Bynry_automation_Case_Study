1. Introduction

This document outlines the test plan for the B2B SaaS platform "WorkFlow Pro".

2. Scope

The scope of this test plan includes:
Part 1: Flaky Test Analysis : Identifying and refactoring unstable tests.
Part 2: Framework Design : Architecting a scalable test automation framework.
Part 3: End-to-End Flow Validation : Testing the complete project creation flow from API to UI and ensuring tenant security.

 3. Testing Approach

Part 1: Flaky Test Analysis

Objective: To refactor unreliable tests to ensure consistent results in the CI/CD pipeline.
Identified Issues:
    Tests lacked explicit waits, causing failures when elements loaded dynamically.
    No handling for potential 2FA screens.
    No error handling for timeouts or unexpected exceptions.
Solution:
  Implement reusable functions for common actions like login.
  Use Playwright's `expect()` for auto-retrying waits to handle dynamic content.
  Incorporate `try...except` blocks for robust error handling.
  Use `@pytest.mark.parametrize` to make tests data-driven and scalable.

Part 2: Test Framework Design

Objective: To design a scalable and maintainable automation framework using the Page Object Model (POM).
Key Directories:
    `tests/`: Contains all test scripts, categorized by type (UI, API, E2E).
    `page_objects/`: Holds classes for each application page to centralize UI locators and actions.
    `utils/`: Reusable helper scripts for API clients, config management, etc.
    `config/` & `test_data/`: Separates environment settings from test input data.
    `.env`**: For storing secrets and credentials securely.

Part 3: API + UI Integration Test

Objective: To validate the complete end-to-end flow of creating a project and verifying its visibility and security.
Test Steps:
    1.  API Creation: Create a project via a `POST` request to `/api/v1/projects`. This is fast and reliable for test setup.
    2.  Web UI Verification: Log in as a user from the same tenant and verify the project appears on the dashboard.
    3.  Mobile UI Verification: Simulate a mobile viewport to check for responsive design and element visibility.
    4.  Tenant Isolation Check: Log in as a user from a different tenant and assert that the project is not visible, ensuring data security.
