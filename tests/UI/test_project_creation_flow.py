import pytest
import uuid
from playwright.sync_api import Page, expect
import re
# from utils.api_client import APIClient # Assumed custom API client

# Define test data for two different tenants
TENANT_1 = {"id": "company1", "user": "manager@company1.com", "pass": "password123"}
TENANT_2 = {"id": "company2", "user": "user@company2.com", "pass": "password456"}

@pytest.fixture(scope="function")
def api_client_t1():
    """Fixture to provide an authenticated API client for Tenant 1."""
    # In a real scenario, this would be a fully implemented API client
    # client = APIClient(tenant_id=TENANT_1["id"])
    # client.authenticate(TENANT_1["user"], TENANT_1["pass"])
    # return client
    pass # Placeholder for demonstration

@pytest.fixture(scope="function")
def project_data_t1(api_client_t1):
    """Sets up test data by creating a project via API and handles cleanup."""
    project_name = f"Project-{uuid.uuid4()}"
    project = {"id": 123, "name": project_name}
    
    # --- Setup ---
    print(f"Simulating API project creation for: {project['name']}")
    # response = api_client_t1.create_project({"name": project_name})
    # assert response.status_code == 201
    # project = response.json()
    
    yield project
    
    # --- Teardown ---
    print(f"Cleaning up project ID: {project['id']}")
    # cleanup_response = api_client_t1.delete_project(project['id'])
    # assert cleanup_response.status_code in [200, 204]

def test_project_creation_and_isolation_flow(page: Page, project_data_t1):
    """End-to-end test for project creation and tenant isolation."""
    
    # Step 2: Web UI - Verify project display for Company1
    page.goto("/login")
    page.get_by_placeholder("Email").fill(TENANT_1["user"])
    page.get_by_placeholder("Password").fill(TENANT_1["pass"])
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r".*/dashboard"))
    new_project_card = page.locator(f".project-card:has-text('{project_data_t1['name']}')")
    expect(new_project_card).to_be_visible(timeout=10000)
    print(f"SUCCESS: Project '{project_data_t1['name']}' is visible in UI for Tenant 1.")
    
    # Step 3: Mobile - Check mobile accessibility
    print("Simulating mobile view check...")
    page.set_viewport_size({"width": 390, "height": 844})
    page.reload()
    mobile_project_card = page.locator(f".project-card:has-text('{project_data_t1['name']}')")
    expect(mobile_project_card).to_be_visible()
    print(f"SUCCESS: Project '{project_data_t1['name']}' is visible in mobile viewport.")
    
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.get_by_role("button", name="Logout").click()
    expect(page).to_have_url(re.compile(r".*/login"))
    
    # Step 4: Security - Verify tenant isolation
    page.get_by_placeholder("Email").fill(TENANT_2["user"])
    page.get_by_placeholder("Password").fill(TENANT_2["pass"])
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r".*/dashboard"))
    isolated_project_card = page.locator(f".project-card:has-text('{project_data_t1['name']}')")
    expect(isolated_project_card).to_be_hidden()
    print(f"SUCCESS: Project '{project_data_t1['name']}' is NOT visible for Tenant 2.")
