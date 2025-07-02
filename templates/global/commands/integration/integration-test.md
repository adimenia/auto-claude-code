# Integration Test

Create comprehensive integration test suites to validate system component interactions and end-to-end workflows.

## Usage:
`/project:integration-test [--scope] [--environment] [--coverage]` or `/user:integration-test [--scope]`

## Process:
1. **Test Planning**: Identify integration points and critical user journeys
2. **Environment Setup**: Configure isolated testing environment with dependencies
3. **Test Data Management**: Create realistic test datasets and mock services
4. **API Testing**: Test service-to-service communication and data flow
5. **Database Integration**: Validate data persistence and transaction integrity
6. **External Service Testing**: Test third-party integrations with mocks/stubs
7. **End-to-End Scenarios**: Implement complete user workflow testing
8. **Performance Validation**: Ensure integration performance meets requirements

## Integration Test Types:
- **API Integration**: Service-to-service API communication
- **Database Integration**: Data layer and ORM testing
- **External Service Integration**: Third-party service interactions
- **Message Queue Integration**: Asynchronous messaging and event handling
- **File System Integration**: File upload, processing, and storage
- **Authentication Integration**: User authentication and authorization flows

## Framework-Specific Testing:
- **FastAPI**: API endpoint testing, dependency injection, async operations
- **Django**: View integration, ORM testing, middleware, form processing
- **Flask**: Blueprint integration, request handling, session management
- **Data Science**: Data pipeline testing, model integration, batch processing

## Arguments:
- `--scope`: Test scope (api, database, external, end-to-end, all)
- `--environment`: Test environment (local, staging, integration, sandbox)
- `--coverage`: Coverage requirements (basic, standard, comprehensive)
- `--parallel`: Enable parallel test execution for faster runs

## Examples:
- `/project:integration-test` - Full integration test suite
- `/project:integration-test --scope api --coverage comprehensive` - API-focused comprehensive testing
- `/project:integration-test --environment staging --parallel` - Staging environment with parallel execution
- `/user:integration-test --scope external` - External service integration testing

## API Integration Testing:

### FastAPI Integration Tests:
```python
import pytest
import httpx
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import User, Post

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create test client with database override."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def authenticated_client(client):
    """Create authenticated test client."""
    # Create test user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    client.post("/auth/register", json=user_data)
    
    # Login and get token
    login_response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword123"
    })
    token = login_response.json()["access_token"]
    
    # Return client with auth headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

class TestUserWorkflow:
    """Test complete user workflow integration."""
    
    def test_user_registration_and_profile_creation(self, client):
        """Test user registration to profile creation flow."""
        # Step 1: Register user
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "full_name": "New User"
        }
        
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]
        
        # Step 2: Login
        login_response = client.post("/auth/login", data={
            "username": "newuser",
            "password": "securepassword123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Step 3: Access protected profile
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = client.get(f"/users/{user_id}/profile", headers=headers)
        assert profile_response.status_code == 200
        assert profile_response.json()["username"] == "newuser"
        
        # Step 4: Update profile
        update_data = {"bio": "Integration test user", "location": "Test City"}
        update_response = client.patch(f"/users/{user_id}/profile", 
                                     json=update_data, headers=headers)
        assert update_response.status_code == 200
        assert update_response.json()["bio"] == "Integration test user"
    
    def test_post_creation_and_interaction_flow(self, authenticated_client):
        """Test post creation, editing, and interaction workflow."""
        # Step 1: Create post
        post_data = {
            "title": "Integration Test Post",
            "content": "This is a test post for integration testing",
            "tags": ["test", "integration"]
        }
        
        create_response = authenticated_client.post("/posts", json=post_data)
        assert create_response.status_code == 201
        post_id = create_response.json()["id"]
        
        # Step 2: Retrieve post
        get_response = authenticated_client.get(f"/posts/{post_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Integration Test Post"
        
        # Step 3: Add comment
        comment_data = {"content": "Great post!"}
        comment_response = authenticated_client.post(f"/posts/{post_id}/comments", 
                                                   json=comment_data)
        assert comment_response.status_code == 201
        
        # Step 4: Like post
        like_response = authenticated_client.post(f"/posts/{post_id}/like")
        assert like_response.status_code == 200
        
        # Step 5: Verify interactions
        post_with_interactions = authenticated_client.get(f"/posts/{post_id}")
        post_data = post_with_interactions.json()
        assert post_data["like_count"] == 1
        assert len(post_data["comments"]) == 1
```

### Database Integration Testing:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User, Post, Comment
from app.services import UserService, PostService

class TestDatabaseIntegration:
    """Test database operations and transactions."""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Setup test database for each test."""
        engine = create_engine("sqlite:///./test_integration.db")
        Base.metadata.create_all(bind=engine)
        
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = TestingSessionLocal()
        
        yield
        
        self.db.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_user_post_relationship_integrity(self):
        """Test user-post relationship and cascading operations."""
        # Create user
        user_service = UserService(self.db)
        user = user_service.create_user({
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        
        # Create posts for user
        post_service = PostService(self.db)
        post1 = post_service.create_post(user.id, {
            "title": "First Post",
            "content": "Content of first post"
        })
        post2 = post_service.create_post(user.id, {
            "title": "Second Post",
            "content": "Content of second post"
        })
        
        # Verify relationships
        assert len(user.posts) == 2
        assert post1.author_id == user.id
        assert post2.author_id == user.id
        
        # Test cascading delete
        user_service.delete_user(user.id)
        
        # Verify posts are also deleted (if cascade is configured)
        remaining_posts = self.db.query(Post).filter(Post.author_id == user.id).all()
        assert len(remaining_posts) == 0
    
    def test_transaction_rollback_on_error(self):
        """Test transaction rollback on database errors."""
        user_service = UserService(self.db)
        
        try:
            with self.db.begin():
                # Create user
                user = user_service.create_user({
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "password123"
                })
                
                # Attempt to create duplicate user (should fail)
                user_service.create_user({
                    "username": "testuser",  # Duplicate username
                    "email": "test2@example.com",
                    "password": "password456"
                })
        except Exception:
            pass  # Expected to fail
        
        # Verify no users were created due to rollback
        user_count = self.db.query(User).count()
        assert user_count == 0
```

### External Service Integration Testing:
```python
import pytest
import responses
import httpx
from unittest.mock import patch
from app.services import EmailService, PaymentService, NotificationService

class TestExternalServiceIntegration:
    """Test integration with external services using mocks."""
    
    @responses.activate
    def test_email_service_integration(self):
        """Test email service integration with mocked responses."""
        # Mock email service API
        responses.add(
            responses.POST,
            "https://api.emailservice.com/send",
            json={"status": "sent", "id": "email_123"},
            status=200
        )
        
        email_service = EmailService()
        result = email_service.send_email(
            to="test@example.com",
            subject="Test Email",
            body="This is a test email"
        )
        
        assert result["status"] == "sent"
        assert "id" in result
    
    @patch('stripe.PaymentIntent.create')
    def test_payment_service_integration(self, mock_payment_create):
        """Test payment service integration with mocked Stripe."""
        # Mock Stripe payment response
        mock_payment_create.return_value = {
            "id": "pi_123456789",
            "status": "succeeded",
            "amount": 2000,
            "currency": "usd"
        }
        
        payment_service = PaymentService()
        result = payment_service.create_payment(
            amount=2000,
            currency="usd",
            customer_id="cus_123"
        )
        
        assert result["status"] == "succeeded"
        assert result["amount"] == 2000
    
    @pytest.mark.asyncio
    async def test_notification_service_integration(self):
        """Test real-time notification service integration."""
        notification_service = NotificationService()
        
        # Test WebSocket connection
        async with notification_service.connect() as websocket:
            # Send test notification
            await notification_service.send_notification(
                user_id="user_123",
                message="Test notification",
                type="info"
            )
            
            # Verify notification received
            notification = await websocket.receive_json()
            assert notification["message"] == "Test notification"
            assert notification["type"] == "info"
```

## End-to-End Testing:

### Selenium Web Testing:
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class TestEndToEndWorkflow:
    """End-to-end testing using Selenium."""
    
    @pytest.fixture
    def browser(self):
        """Setup browser for testing."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless in CI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        
        driver.quit()
    
    def test_complete_user_journey(self, browser):
        """Test complete user journey from registration to content creation."""
        base_url = "http://localhost:3000"
        
        # Step 1: Navigate to registration
        browser.get(f"{base_url}/register")
        
        # Step 2: Fill registration form
        browser.find_element(By.NAME, "username").send_keys("e2euser")
        browser.find_element(By.NAME, "email").send_keys("e2e@example.com")
        browser.find_element(By.NAME, "password").send_keys("password123")
        browser.find_element(By.NAME, "confirmPassword").send_keys("password123")
        
        # Step 3: Submit registration
        browser.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Step 4: Verify redirect to dashboard
        WebDriverWait(browser, 10).until(
            EC.url_contains("/dashboard")
        )
        assert "/dashboard" in browser.current_url
        
        # Step 5: Create new post
        browser.find_element(By.LINK_TEXT, "Create Post").click()
        browser.find_element(By.NAME, "title").send_keys("E2E Test Post")
        browser.find_element(By.NAME, "content").send_keys("This is an end-to-end test post")
        browser.find_element(By.XPATH, "//button[text()='Publish']").click()
        
        # Step 6: Verify post creation
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TEXT, "E2E Test Post"))
        )
        assert "E2E Test Post" in browser.page_source
    
    def test_responsive_design_workflow(self, browser):
        """Test workflow across different screen sizes."""
        base_url = "http://localhost:3000"
        
        # Test desktop view
        browser.set_window_size(1920, 1080)
        browser.get(base_url)
        
        # Verify desktop navigation
        desktop_nav = browser.find_element(By.CLASS_NAME, "desktop-nav")
        assert desktop_nav.is_displayed()
        
        # Test mobile view
        browser.set_window_size(375, 667)
        browser.refresh()
        
        # Verify mobile navigation
        mobile_nav = browser.find_element(By.CLASS_NAME, "mobile-nav")
        assert mobile_nav.is_displayed()
        
        # Test mobile menu functionality
        menu_button = browser.find_element(By.CLASS_NAME, "menu-toggle")
        menu_button.click()
        
        mobile_menu = browser.find_element(By.CLASS_NAME, "mobile-menu")
        assert mobile_menu.is_displayed()
```

## Performance Integration Testing:

### Load Testing with Real Dependencies:
```python
import asyncio
import aiohttp
import time
from typing import List, Dict

class IntegrationLoadTester:
    """Load testing with real service dependencies."""
    
    def __init__(self, base_url: str, concurrency: int = 10):
        self.base_url = base_url
        self.concurrency = concurrency
        self.results = []
    
    async def test_user_workflow_under_load(self):
        """Test complete user workflow under concurrent load."""
        tasks = []
        
        for i in range(self.concurrency):
            task = asyncio.create_task(
                self.simulate_user_session(f"loadtest_user_{i}")
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Analyze results
        successful_sessions = [r for r in results if not isinstance(r, Exception)]
        failed_sessions = [r for r in results if isinstance(r, Exception)]
        
        success_rate = len(successful_sessions) / len(results) * 100
        avg_duration = sum(s['total_duration'] for s in successful_sessions) / len(successful_sessions)
        
        return {
            "success_rate": success_rate,
            "average_duration": avg_duration,
            "total_sessions": len(results),
            "failed_sessions": len(failed_sessions)
        }
    
    async def simulate_user_session(self, username: str) -> Dict:
        """Simulate complete user session."""
        start_time = time.time()
        session_data = {"username": username, "steps": []}
        
        async with aiohttp.ClientSession() as session:
            try:
                # Step 1: Register user
                register_start = time.time()
                register_data = {
                    "username": username,
                    "email": f"{username}@loadtest.com",
                    "password": "password123"
                }
                
                async with session.post(f"{self.base_url}/auth/register", 
                                      json=register_data) as resp:
                    if resp.status == 201:
                        session_data["steps"].append({
                            "step": "register",
                            "duration": time.time() - register_start,
                            "success": True
                        })
                
                # Step 2: Login
                login_start = time.time()
                async with session.post(f"{self.base_url}/auth/login",
                                      data={"username": username, "password": "password123"}) as resp:
                    if resp.status == 200:
                        token_data = await resp.json()
                        token = token_data["access_token"]
                        session_data["steps"].append({
                            "step": "login",
                            "duration": time.time() - login_start,
                            "success": True
                        })
                
                # Step 3: Create posts
                headers = {"Authorization": f"Bearer {token}"}
                for i in range(3):
                    post_start = time.time()
                    post_data = {
                        "title": f"Load Test Post {i}",
                        "content": f"Content for post {i} by {username}"
                    }
                    
                    async with session.post(f"{self.base_url}/posts",
                                          json=post_data, headers=headers) as resp:
                        if resp.status == 201:
                            session_data["steps"].append({
                                "step": f"create_post_{i}",
                                "duration": time.time() - post_start,
                                "success": True
                            })
                
                session_data["total_duration"] = time.time() - start_time
                return session_data
                
            except Exception as e:
                session_data["error"] = str(e)
                session_data["total_duration"] = time.time() - start_time
                raise e
```

## Validation Checklist:
- [ ] All integration points identified and tested
- [ ] Database transactions and rollbacks tested
- [ ] External service integrations mocked appropriately
- [ ] End-to-end user workflows validated
- [ ] Error handling and edge cases covered
- [ ] Performance under load validated
- [ ] Test data management and cleanup implemented
- [ ] Cross-browser and responsive design tested
- [ ] Security integration (authentication/authorization) verified
- [ ] Monitoring and logging integration tested

## Output:
- Comprehensive integration test suite with multiple test types
- Database integration tests with transaction management
- External service integration tests with proper mocking
- End-to-end workflow tests using browser automation
- Performance integration tests under realistic load
- Test data management and cleanup procedures
- CI/CD integration for automated testing
- Test reporting and coverage analysis
- Documentation for test maintenance and extension

## Notes:
- Use test databases that mirror production schema
- Implement proper test data cleanup between test runs
- Mock external services to avoid dependencies and costs
- Use realistic test data volumes for performance testing
- Implement parallel test execution for faster feedback
- Monitor test execution time and optimize slow tests
- Maintain integration tests as application evolves
- Consider using containerized environments for consistent testing