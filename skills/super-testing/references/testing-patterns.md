# Testing Patterns & Anti-Patterns

## Core Testing Patterns

### 1. AAA Pattern (Arrange-Act-Assert)

```python
def test_user_creation():
    # Arrange: Set up test data
    user_data = {
        "email": "test@example.com",
        "password": "secure123"
    }
    
    # Act: Execute the code under test
    user = create_user(user_data)
    
    # Assert: Verify the result
    assert user.id is not None
    assert user.email == user_data["email"]
```

### 2. Given-When-Then (BDD Style)

```python
def test_user_login():
    # Given: A registered user
    user = create_user("test@example.com", "password123")
    
    # When: User logs in
    result = login("test@example.com", "password123")
    
    # Then: Login should succeed
    assert result.success is True
    assert result.token is not None
```

### 3. Four-Phase Test

```python
def test_database_query():
    # 1. Setup
    db = Database()
    db.connect()
    
    # 2. Exercise
    result = db.query("SELECT * FROM users")
    
    # 3. Verify
    assert len(result) > 0
    
    # 4. Teardown
    db.disconnect()
```

### 4. Test Fixture Pattern

```python
@pytest.fixture
def sample_user():
    """Reusable test data."""
    return User(email="test@example.com", name="Test User")

def test_with_fixture(sample_user):
    assert sample_user.email == "test@example.com"
```

### 5. Object Mother Pattern

```python
class UserMother:
    """Factory for creating test users."""
    
    @staticmethod
    def create(**overrides):
        defaults = {
            "email": "test@example.com",
            "name": "Test User",
            "role": "user"
        }
        defaults.update(overrides)
        return User(**defaults)
    
    @staticmethod
    def admin():
        return UserMother.create(role="admin", email="admin@example.com")

def test_admin_permissions():
    admin = UserMother.admin()
    assert admin.has_permission("delete_users")
```

### 6. Builder Pattern for Complex Objects

```python
class OrderBuilder:
    def __init__(self):
        self.items = []
        self.customer = None
        self.shipping = "standard"
    
    def with_items(self, *items):
        self.items.extend(items)
        return self
    
    def with_customer(self, customer):
        self.customer = customer
        return self
    
    def with_express_shipping(self):
        self.shipping = "express"
        return self
    
    def build(self):
        return Order(
            items=self.items,
            customer=self.customer,
            shipping=self.shipping
        )

# Usage
order = (OrderBuilder()
    .with_items(item1, item2)
    .with_customer(customer)
    .with_express_shipping()
    .build())
```

### 7. Mock Object Pattern

```python
class MockEmailService:
    def __init__(self):
        self.sent_emails = []
    
    def send(self, to, subject, body):
        self.sent_emails.append({
            "to": to,
            "subject": subject,
            "body": body
        })
        return True
    
    def assert_email_sent(self, to):
        assert any(e["to"] == to for e in self.sent_emails)

def test_welcome_email():
    email_service = MockEmailService()
    user_service = UserService(email_service)
    
    user_service.register("test@example.com")
    
    email_service.assert_email_sent("test@example.com")
```

### 8. Spy Pattern

```python
class SpyLogger:
    def __init__(self):
        self.calls = []
    
    def info(self, message):
        self.calls.append(("info", message))
    
    def error(self, message):
        self.calls.append(("error", message))

def test_error_logging():
    spy = SpyLogger()
    processor = DataProcessor(logger=spy)
    
    processor.process(invalid_data)
    
    assert any("error" in call for call in spy.calls)
```

### 9. Fake Pattern

```python
class FakeDatabase:
    """In-memory database for testing."""
    
    def __init__(self):
        self.data = {}
        self._next_id = 1
    
    def insert(self, table, record):
        id = self._next_id
        self._next_id += 1
        self.data[(table, id)] = {**record, "id": id}
        return id
    
    def get(self, table, id):
        return self.data.get((table, id))
    
    def delete(self, table, id):
        del self.data[(table, id)]

def test_with_fake_db():
    db = FakeDatabase()
    user_id = db.insert("users", {"name": "Test"})
    
    user = db.get("users", user_id)
    assert user["name"] == "Test"
```

### 10. Parameterized Test Pattern

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("WORLD", "WORLD"),
    ("", ""),
    (None, None),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

## Test Organization Patterns

### 1. Arrange-Act-Assert Comments

```python
def test_password_reset():
    # Arrange
    user = create_user("test@example.com")
    
    # Act
    token = request_password_reset(user.email)
    
    # Assert
    assert token is not None
    assert token.is_valid()
```

### 2. Test Class Grouping

```python
class TestUserRegistration:
    """Tests for user registration flow."""
    
    def test_valid_registration(self):
        pass
    
    def test_duplicate_email(self):
        pass
    
    def test_invalid_email(self):
        pass


class TestUserLogin:
    """Tests for user login."""
    
    def test_valid_login(self):
        pass
    
    def test_wrong_password(self):
        pass
```

### 3. Descriptive Test Names

```python
# Good
def test_user_cannot_login_with_wrong_password():
    pass

def test_admin_can_delete_any_user():
    pass

# Bad
def test_login():
    pass

def test_delete():
    pass
```

## Anti-Patterns to Avoid

### 1. Testing Implementation Details

```python
# Bad: Tests private method
def test_private_helper():
    obj = MyClass()
    assert obj._helper() == "result"

# Good: Tests public behavior
def test_public_interface():
    obj = MyClass()
    assert obj.process() == "expected result"
```

### 2. Hardcoded Values Without Context

```python
# Bad
def test_timeout():
    time.sleep(5000)  # What is 5000?
    assert True

# Good
def test_timeout():
    TIMEOUT_MS = 5000  # 5 seconds timeout
    time.sleep(TIMEOUT_MS / 1000)
    assert True
```

### 3. Testing Multiple Things

```python
# Bad
def test_everything():
    user = create_user("test@example.com")
    assert user.id is not None
    assert user.email == "test@example.com"
    order = create_order(user)
    assert order.id is not None
    payment = process_payment(order)
    assert payment.status == "success"

# Good
def test_user_creation():
    user = create_user("test@example.com")
    assert user.id is not None

def test_order_creation():
    user = create_user("test@example.com")
    order = create_order(user)
    assert order.id is not None
```

### 4. Interdependent Tests

```python
# Bad
created_user = None

def test_create():
    global created_user
    created_user = create_user("test@example.com")

def test_delete():
    delete_user(created_user.id)  # Depends on test_create

# Good
def test_delete():
    user = create_user("delete@example.com")  # Independent
    delete_user(user.id)
    assert get_user(user.id) is None
```

### 5. Magic Numbers

```python
# Bad
assert calculate(100, 0.15) == 15

# Good
PRICE = 100
DISCOUNT_RATE = 0.15
EXPECTED_DISCOUNT = 15
assert calculate(PRICE, DISCOUNT_RATE) == EXPECTED_DISCOUNT
```

### 6. Exception Testing Without Context

```python
# Bad
def test_exception():
    with pytest.raises(ValueError):
        do_something()

# Good
def test_invalid_email_raises_value_error():
    with pytest.raises(ValueError, match="Invalid email"):
        create_user("not-an-email")
```

### 7. Sleep in Tests

```python
# Bad
def test_async():
    start_async_job()
    time.sleep(5)  # Hope it finishes
    assert job_complete()

# Good
def test_async():
    start_async_job()
    wait_for(lambda: job_complete(), timeout=10)
    assert job_complete()
```

### 8. Shared Mutable State

```python
# Bad
shared_list = []

def test_append():
    shared_list.append(1)
    assert len(shared_list) == 1

def test_append_again():
    shared_list.append(2)  # Depends on previous test
    assert len(shared_list) == 2

# Good
def test_append():
    my_list = []
    my_list.append(1)
    assert len(my_list) == 1
```

## Performance Testing Patterns

### 1. Timing Test

```python
import time

def test_response_time():
    start = time.time()
    result = api_call()
    elapsed = time.time() - start
    
    assert elapsed < 1.0  # Must respond within 1 second
```

### 2. Load Test

```python
import concurrent.futures

def test_concurrent_requests():
    def make_request():
        return api_call()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in futures]
    
    success_count = sum(1 for r in results if r.status == 200)
    assert success_count >= 95  # 95% success rate
```

## Security Testing Patterns

### 1. SQL Injection Test

```python
def test_sql_injection():
    malicious_input = "'; DROP TABLE users; --"
    
    with pytest.raises(ValidationError):
        search_users(malicious_input)
```

### 2. XSS Test

```python
def test_xss_prevention():
    xss_payload = "<script>alert('XSS')</script>"
    
    result = sanitize_input(xss_payload)
    
    assert "<script>" not in result
```

### 3. Authentication Test

```python
def test_unauthorized_access():
    response = api_client.get("/admin/users")  # No auth token
    
    assert response.status_code == 401
```

## Summary Table

| Pattern | When to Use |
|---------|-------------|
| AAA | Simple unit tests |
| Given-When-Then | BDD-style tests |
| Object Mother | Reusable test data |
| Builder | Complex object creation |
| Mock | External dependencies |
| Spy | Verify interactions |
| Fake | Replace heavy dependencies |
| Parameterized | Multiple similar test cases |