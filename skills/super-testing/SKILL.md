---
name: super-testing
description: Comprehensive testing skill for Python (pytest), Web applications (Playwright), and E2E testing frameworks. Use when user asks about writing tests, setting up test infrastructure, test strategies, or debugging test failures. Covers unit tests, integration tests, API tests, UI/E2E tests, performance tests, and mocking strategies.
---

# Super Testing Skill

A comprehensive testing skill covering Python testing with pytest, web application testing with Playwright, and modern E2E testing frameworks.

## Table of Contents

1. [Python Testing (pytest)](#python-testing-pytest)
2. [Web Application Testing (Playwright)](#web-application-testing-playwright)
3. [Test Strategy Design](#test-strategy-design)
4. [E2E Testing Framework](#e2e-testing-framework)
5. [Mocking & Fixtures](#mocking--fixtures)
6. [CI/CD Integration](#cicd-integration)

---

## Python Testing (pytest)

### Basic Test Structure

```python
# test_example.py
import pytest

def test_simple_assertion():
    """Simple assertion test."""
    assert 1 + 1 == 2

class TestCalculator:
    """Group related tests in a class."""
    
    def test_add(self):
        assert 2 + 2 == 4
    
    def test_subtract(self):
        assert 5 - 3 == 2
```

### Pytest Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide test data."""
    return {"name": "test", "value": 42}

@pytest.fixture
def db_connection():
    """Setup and teardown database connection."""
    conn = create_connection()
    yield conn
    conn.close()

def test_with_fixture(sample_data):
    assert sample_data["value"] == 42

def test_with_db(db_connection):
    result = db_connection.query("SELECT 1")
    assert result is not None
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected

@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiple_params(x, y):
    assert x * y > 0
```

### Markers

```python
@pytest.mark.slow
def test_slow_operation():
    """Mark slow tests."""
    time.sleep(5)
    assert True

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_expected_failure():
    assert False
```

---

## Web Application Testing (Playwright)

### Basic Page Operations

```typescript
import { test, expect } from '@playwright/test';

test('page title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

test('click and navigate', async ({ page }) => {
  await page.goto('https://example.com');
  await page.click('text=More information');
  await expect(page).toHaveURL(/iana/);
});
```

### Form Handling

```typescript
test('fill form', async ({ page }) => {
  await page.goto('/login');
  
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('.welcome')).toBeVisible();
});
```

### API Testing

```typescript
test('API endpoint', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.ok()).toBeTruthy();
  
  const users = await response.json();
  expect(users.length).toBeGreaterThan(0);
});

test('POST request', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'New User', email: 'new@example.com' }
  });
  expect(response.status()).toBe(201);
});
```

### Visual Regression

```typescript
test('visual snapshot', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png');
});
```

---

## Test Strategy Design

### Testing Pyramid

```
        /\
       /  \      E2E Tests (Few, Slow, Expensive)
      /----\     
     /      \    Integration Tests (Some, Medium)
    /--------\
   /          \  Unit Tests (Many, Fast, Cheap)
  /------------\
```

### Test Categories

| Category | Purpose | Speed | Count |
|----------|---------|-------|-------|
| Unit | Test individual functions | Fast | Many |
| Integration | Test component interactions | Medium | Some |
| E2E | Test complete user flows | Slow | Few |
| Performance | Test load & response times | Varies | Selective |
| Security | Test vulnerabilities | Medium | Critical paths |

### Coverage Strategy

```python
# Run with coverage
# pytest --cov=src --cov-report=html --cov-report=term

# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */__pycache__/*
    
[report]
exclude_lines =
    pragma: no cover
    if TYPE_CHECKING:
    raise NotImplementedError
```

---

## E2E Testing Framework

### Test Flow Pattern

```typescript
// e2e/user-journey.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Journey', () => {
  test('complete purchase flow', async ({ page }) => {
    // 1. Login
    await page.goto('/login');
    await page.fill('[name=email]', 'user@test.com');
    await page.fill('[name=password]', 'password');
    await page.click('button:has-text("Sign In")');
    
    // 2. Browse products
    await page.click('text=Products');
    await expect(page.locator('.product-grid')).toBeVisible();
    
    // 3. Add to cart
    await page.click('.product:first-child .add-to-cart');
    await expect(page.locator('.cart-count')).toHaveText('1');
    
    // 4. Checkout
    await page.click('text=Checkout');
    await page.fill('[name=card]', '4242424242424242');
    await page.click('button:has-text("Place Order")');
    
    // 5. Verify success
    await expect(page.locator('.order-confirmation')).toBeVisible();
  });
});
```

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}
  
  async goto() {
    await this.page.goto('/login');
  }
  
  async login(email: string, password: string) {
    await this.page.fill('[name=email]', email);
    await this.page.fill('[name=password]', password);
    await this.page.click('button:has-text("Sign In")');
  }
  
  async getErrorMessage() {
    return this.page.locator('.error-message').textContent();
  }
}

// Usage
test('login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@test.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

---

## Mocking & Fixtures

### Python Mocking

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_service = Mock()
    mock_service.get_data.return_value = {"status": "ok"}
    
    result = mock_service.get_data()
    assert result["status"] == "ok"
    mock_service.get_data.assert_called_once()

@patch('module.external_api')
def test_with_patch(mock_api):
    mock_api.return_value = {"data": "mocked"}
    # Test code that uses external_api
```

### Playwright Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';

type MyFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup: login
    await page.goto('/login');
    await page.fill('[name=email]', 'test@example.com');
    await page.fill('[name=password]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    
    await use(page);
    
    // Teardown: logout
    await page.click('text=Logout');
  },
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### Playwright CI

```yaml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run Playwright tests
  run: npx playwright test

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-report
    path: playwright-report/
```

---

## Best Practices

### Test Naming

```python
# Good: descriptive and specific
def test_user_login_with_valid_credentials():
    pass

def test_user_login_fails_with_wrong_password():
    pass

# Bad: vague
def test_login():
    pass
```

### AAA Pattern

```python
def test_user_registration():
    # Arrange
    user_data = {"email": "test@example.com", "password": "secure123"}
    
    # Act
    result = register_user(user_data)
    
    # Assert
    assert result.success is True
    assert result.user.email == user_data["email"]
```

### Test Independence

```python
# Good: each test is independent
def test_create_user():
    user = create_user("test@example.com")
    assert user.id is not None

def test_delete_user():
    user = create_user("delete@example.com")  # Create fresh user
    delete_user(user.id)
    assert get_user(user.id) is None

# Bad: tests depend on each other
def test_create_user():
    global created_user
    created_user = create_user("test@example.com")

def test_delete_user():
    delete_user(created_user.id)  # Depends on previous test
```

---

## Scripts Reference

The `scripts/` directory contains executable scripts for common testing tasks:

- `run-pytest.sh` - Run Python tests with coverage
- `run-playwright.sh` - Run Playwright E2E tests
- `run-e2e.sh` - Run full E2E test suite

## References

The `references/` directory contains detailed guides:

- `pytest-guide.md` - Comprehensive pytest documentation
- `playwright-guide.md` - Playwright best practices
- `testing-patterns.md` - Common testing patterns and anti-patterns

## Assets

The `assets/` directory contains configuration templates:

- `pytest.ini.template` - pytest configuration
- `playwright.config.ts.template` - Playwright configuration
- `vitest.config.ts.template` - Vitest configuration for frontend tests