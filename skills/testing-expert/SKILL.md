---
name: testing-expert
description: Comprehensive testing expert for Python and web applications. Use when implementing tests (unit/integration/e2e), designing test strategies, setting up pytest or Playwright, writing fixtures, mocking dependencies, debugging flaky tests, or configuring CI/CD testing pipelines.
license: MIT
---

# Testing Expert

A unified testing skill that combines:
- **Python Testing Patterns**: Unit tests, fixtures, mocking, TDD, pytest best practices
- **Test Strategy Design**: Test pyramid, coverage planning, CI/CD integration
- **Web Application Testing**: Playwright automation, UI testing, browser debugging

## When to Use This Skill

### Strategy & Planning
- Designing test strategy for new/existing projects
- Setting up test infrastructure and CI/CD
- Planning test coverage and test pyramid
- Implementing TDD practices

### Python Testing
- Writing unit tests, integration tests
- Setting up pytest and fixtures
- Mocking external dependencies
- Testing async code and databases
- Property-based testing

### Web Application Testing
- Browser automation with Playwright
- E2E testing for web apps
- UI behavior verification
- Capturing screenshots and logs

## Core Concepts

### 1. Test Pyramid Strategy

```
       /\            E2E Tests (10%) - Critical user flows
      /  \           - Slow, expensive
     /────\          - Run before deployment
    /      \         
   /Integration\     Integration Tests (20%) - API + DB
  /────────────\     - Medium speed
 /              \    
/   Unit Tests   \   Unit Tests (70%) - Business logic
/________________\  - Fast, inexpensive
                    - Run every commit
```

**Coverage Goals**:
- Unit Tests: 80%+ coverage
- Integration Tests: 60%+ coverage  
- E2E Tests: Critical user flows

### 2. Test Structure (AAA/GWT Pattern)

**AAA (Arrange-Act-Assert)**:
```python
def test_user_creation():
    # Arrange
    user_data = {"name": "John", "email": "john@example.com"}
    
    # Act
    user = create_user(user_data)
    
    # Assert
    assert user.id is not None
    assert user.name == "John"
```

**Given-When-Then**:
```python
def test_discount_calculation():
    # Given
    order = {"total": 150, "customer_id": "123"}
    
    # When
    discount = calculate_discount(order)
    
    # Then
    assert discount == 15
```

## Python Testing Guide

### Basic pytest Tests

```python
import pytest

# Simple test
def test_addition():
    assert add(2, 3) == 5

# Test with exception
def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# Parameterized test
@pytest.mark.parametrize("input,expected", [
    ("user@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_email_validation(input, expected):
    assert is_valid_email(input) == expected
```

### Fixtures for Setup/Teardown

```python
@pytest.fixture
def db_session():
    """Create isolated database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = SessionLocal(bind=engine)
    yield session
    session.close()

def test_create_user(db_session):
    user = User(name="Test")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

@patch("requests.get")
def test_api_call(mock_get):
    # Setup mock
    mock_get.return_value.json.return_value = {"id": 1}
    
    # Execute
    result = fetch_user(1)
    
    # Verify
    assert result["id"] == 1
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### Async Code Testing

```python
@pytest.mark.asyncio
async def test_async_operation():
    result = await fetch_data("url")
    assert result is not None

@pytest.mark.asyncio
async def test_concurrent_operations():
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    assert len(results) == len(urls)
```

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_reverse_twice_is_original(s):
    """Property: reversing twice returns original."""
    assert reverse(reverse(s)) == s

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Property: a + b == b + a"""
    assert add(a, b) == add(b, a)
```

## Web Application Testing (Playwright)

### Basic Automation Pattern

```python
from playwright.sync_api import sync_playwright

def test_user_registration():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate and wait for JS
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')
        
        # Take screenshot for debugging
        page.screenshot(path='/tmp/before.png')
        
        # Execute actions
        page.click('text=Sign Up')
        page.fill('input[name="email"]', 'test@example.com')
        page.fill('input[name="password"]', 'Password123!')
        page.click('button[type="submit"]')
        
        # Verify result
        assert page.url == 'http://localhost:3000/dashboard'
        assert page.locator('text=Welcome').is_visible()
        
        browser.close()
```

### Server Management

**Single server**:
```bash
python scripts/with_server.py \
  --server "npm run dev" --port 5173 \
  -- python your_test.py
```

**Multiple servers**:
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_test.py
```

### Reconnaissance-Then-Action Pattern

```python
# 1. Inspect rendered DOM
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')
page.screenshot(path='/tmp/inspect.png')
content = page.content()

# 2. Identify selectors
buttons = page.locator('button').all()
links = page.locator('a').all()

# 3. Execute actions
for btn in buttons:
    if btn.is_visible():
        btn.click()
```

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

```python
# 1. RED: Write failing test
def test_password_strength():
    assert is_strong_password("weak") == False
    assert is_strong_password("Str0ng!Pass") == True

# 2. GREEN: Minimal implementation
def is_strong_password(password):
    if len(password) < 8:
        return False
    return True

# 3. REFACTOR: Improve code
def is_strong_password(password):
    """Check if password meets security requirements."""
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)
    return all([has_upper, has_lower, has_digit, has_special])

# 4. Add more test cases
def test_password_edge_cases():
    assert is_strong_password("") == False
    assert is_strong_password("12345678") == False
    assert is_strong_password("Password1!") == True
```

## Integration Testing

### API Testing

```python
import requests

def test_create_user_api():
    response = requests.post(
        "http://localhost:3000/api/users",
        json={"email": "test@example.com", "name": "Test"}
    )
    
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    
    # Verify in database
    user = db.query(User).filter_by(email="test@example.com").first()
    assert user is not None
```

### Database Testing

```python
@pytest.fixture
def clean_db():
    """Reset database before each test."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield

def test_user_persistence(clean_db):
    user = User(email="test@example.com")
    db.add(user)
    db.commit()
    
    retrieved = db.query(User).filter_by(email="test@example.com").first()
    assert retrieved is not None
```

## Best Practices

### Test Organization

```
tests/
├── unit/              # Unit tests (fast, isolated)
│   ├── test_models.py
│   └── test_utils.py
├── integration/       # Integration tests (API, DB)
│   ├── test_api.py
│   └── test_database.py
├── e2e/              # End-to-end tests (browser)
│   └── test_user_flow.py
└── conftest.py       # Shared fixtures
```

### Test Naming Convention

```python
# Pattern: test_<unit>_<scenario>_<expected>
def test_create_user_with_valid_data_returns_user():
    pass

def test_create_user_with_duplicate_email_raises_conflict():
    pass

def test_login_with_invalid_password_fails():
    pass
```

### Test Isolation Rules

✅ **DO**:
- Each test is independent
- Clean up after each test
- Use fresh fixtures
- Mock external dependencies

❌ **DON'T**:
- Share state between tests
- Use production database
- Depend on test execution order
- Use sleep() or timeouts

## CI/CD Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -e ".[dev]"
      
      - name: Run unit tests
        run: pytest tests/unit -v --cov=app
      
      - name: Run integration tests
        run: pytest tests/integration -v
      
      - name: Run E2E tests
        run: pytest tests/e2e -v
```

### Coverage Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
addopts = 
    -v 
    --cov=app 
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    slow: marks tests as slow
    integration: marks integration tests
    e2e: marks end-to-end tests
```

## Common Testing Patterns

### Testing Exceptions

```python
def test_invalid_input_raises_error():
    with pytest.raises(ValueError, match="Invalid email"):
        validate_email("not-an-email")
```

### Testing Time-Dependent Code

```python
from freezegun import freeze_time

@freeze_time("2024-01-15 10:00:00")
def test_token_expiry():
    token = create_token(expires_in=3600)
    assert token.expires_at == datetime(2024, 1, 15, 11, 0, 0)
```

### Testing Retry Logic

```python
def test_retries_on_failure():
    mock_client = Mock()
    mock_client.request.side_effect = [
        ConnectionError("Failed"),
        ConnectionError("Failed"),
        {"status": "ok"}
    ]
    
    result = service_with_retry(mock_client).fetch()
    assert result == {"status": "ok"}
    assert mock_client.request.call_count == 3
```

## Decision Flowchart

```
Need to test? → What type?
    │
    ├─ Business logic → Unit test
    │   └─ Use pytest + fixtures
    │
    ├─ API/Database → Integration test
    │   └─ Use test DB + API client
    │
    └─ User flow → E2E test
        └─ Use Playwright
```

## Quick Reference

### Test Execution Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_models.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest -m unit

# Run slow tests
pytest -m slow

# Run in parallel
pytest -n auto

# Stop on first failure
pytest -x
```

### Playwright Commands

```bash
# Run Playwright tests
pytest tests/e2e

# Run in headed mode (see browser)
pytest tests/e2e --headed

# Debug mode
pytest tests/e2e --debug

# Generate code
playwright codegen http://localhost:3000
```

## Troubleshooting

### Common Issues

**Tests fail intermittently**:
- Check for race conditions
- Use proper waits (not sleep)
- Ensure test isolation

**Coverage too low**:
- Identify missing tests with `--cov-report=term-missing`
- Focus on critical paths first
- Don't chase 100% - aim for meaningful coverage

**E2E tests flaky**:
- Always wait for `networkidle`
- Use explicit waits for elements
- Avoid timing-dependent assertions

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/python/)
- [Test Pyramid - Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Hypothesis - Property-based Testing](https://hypothesis.works/)

---

## Bundled Resources

### Scripts

Executable scripts for running tests:

| Script | Description | Usage |
|--------|-------------|-------|
| `scripts/run-pytest.sh` | Run pytest with coverage, parallelization, and threshold checking | `./run-pytest.sh tests/unit` |
| `scripts/run-playwright.sh` | Run Playwright tests with optional server management | `./run-playwright.sh --server "npm run dev"` |

**When to use scripts:**
- Use `run-pytest.sh` for quick test execution with sensible defaults
- Use `run-playwright.sh` when you need to start a dev server before running E2E tests

### Reference Documentation

Detailed patterns and examples (read as needed):

| Reference | Content | When to Read |
|-----------|---------|--------------|
| `references/pytest-patterns.md` | Comprehensive pytest patterns: fixtures, parametrization, mocking, async, database testing | When writing complex pytest tests |
| `references/playwright-examples.md` | Playwright patterns: selectors, assertions, page objects, authentication, visual testing | When implementing E2E tests |

### Templates

Ready-to-use configuration templates:

| Template | Purpose | How to Use |
|----------|---------|------------|
| `assets/pytest.ini.template` | pytest configuration with markers, coverage, and logging | Copy to project root as `pytest.ini` |
| `assets/conftest.py.template` | Shared fixtures for database, mocking, and utilities | Copy to `tests/conftest.py` and customize |

---

**This skill provides a complete testing toolkit covering strategy, implementation, and automation across Python and web applications.**