# pytest Patterns Reference

Comprehensive collection of pytest patterns and best practices.

## Table of Contents

1. [Basic Tests](#basic-tests)
2. [Fixtures](#fixtures)
3. [Parametrization](#parametrization)
4. [Mocking](#mocking)
5. [Markers](#markers)
6. [Async Testing](#async-testing)
7. [Database Testing](#database-testing)
8. [API Testing](#api-testing)
9. [Advanced Patterns](#advanced-patterns)

---

## Basic Tests

### Simple Assertions

```python
def test_equality():
    assert 1 + 1 == 2

def test_string_operations():
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert "world" in text

def test_list_operations():
    items = [1, 2, 3]
    assert len(items) == 3
    assert 2 in items
```

### Exception Testing

```python
import pytest

def test_raises_value_error():
    with pytest.raises(ValueError, match="invalid value"):
        raise ValueError("invalid value")

def test_raises_type_error():
    with pytest.raises(TypeError):
        "string" + 123  # TypeError: can only concatenate str to str

def test_custom_exception():
    class CustomError(Exception):
        pass
    
    with pytest.raises(CustomError) as exc_info:
        raise CustomError("Something went wrong")
    
    assert str(exc_info.value) == "Something went wrong"
```

### Warning Testing

```python
import warnings

def test_warning():
    with pytest.warns(UserWarning, match="deprecated"):
        warnings.warn("This is deprecated", UserWarning)
```

---

## Fixtures

### Basic Fixtures

```python
@pytest.fixture
def sample_data():
    return {"name": "test", "value": 42}

def test_with_fixture(sample_data):
    assert sample_data["name"] == "test"
    assert sample_data["value"] == 42
```

### Fixture Scopes

```python
# Run once per test function (default)
@pytest.fixture(scope="function")
def fresh_data():
    return {"counter": 0}

# Run once per test class
@pytest.fixture(scope="class")
def class_data():
    return {"shared": "data"}

# Run once per module
@pytest.fixture(scope="module")
def module_config():
    return load_config()

# Run once per session
@pytest.fixture(scope="session")
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### Fixture with Setup/Teardown

```python
@pytest.fixture
def temp_file():
    # Setup
    import tempfile
    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(b"test content")
    file.close()
    
    yield file.name  # Pass to test
    
    # Teardown
    import os
    os.unlink(file.name)

def test_file_operations(temp_file):
    with open(temp_file) as f:
        content = f.read()
    assert content == "test content"
```

### Fixture Dependencies

```python
@pytest.fixture
def database():
    return {"users": []}

@pytest.fixture
def user_factory(database):
    def create_user(name):
        user = {"id": len(database["users"]) + 1, "name": name}
        database["users"].append(user)
        return user
    return create_user

def test_user_creation(user_factory):
    user = user_factory("Alice")
    assert user["name"] == "Alice"
    assert user["id"] == 1
```

### Autouse Fixtures

```python
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Automatically applied to all tests."""
    monkeypatch.setenv("TEST_MODE", "true")
    yield
    # Cleanup happens automatically
```

---

## Parametrization

### Basic Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
])
def test_addition(x, y, expected):
    assert x + y == expected
```

### Parametrize with IDs

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("", False),
], ids=["valid_email", "invalid_format", "empty_string"])
def test_email_validation(email, valid):
    assert is_valid_email(email) == valid
```

### Nested Parametrization

```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiplication(x, y):
    # Tests all combinations: 1*10, 1*20, 2*10, 2*20, 3*10, 3*20
    assert x * y == x * y  # Trivial example
```

### Conditional Parametrization

```python
import sys

@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(1, 2, marks=pytest.mark.skipif(sys.version_info < (3, 8), reason="needs py3.8+")),
        (2, 4),
        (3, 6),
    ]
)
def test_conditional(value, expected):
    assert value * 2 == expected
```

---

## Mocking

### Basic Mocking

```python
from unittest.mock import Mock, patch

def test_mock_object():
    mock = Mock()
    mock.method.return_value = 42
    
    result = mock.method()
    assert result == 42
    mock.method.assert_called_once()

def test_mock_attributes():
    mock = Mock()
    mock.name = "test"
    mock.value = 100
    
    assert mock.name == "test"
    assert mock.value == 100
```

### Patching Functions

```python
@patch("module.function_name")
def test_patched_function(mock_func):
    mock_func.return_value = "mocked"
    
    result = module.function_name()
    assert result == "mocked"

# Alternative: context manager
def test_patched_with_context():
    with patch("module.function_name") as mock_func:
        mock_func.return_value = "mocked"
        result = module.function_name()
        assert result == "mocked"
```

### Patching Classes

```python
@patch("module.MyClass")
def test_patched_class(MockClass):
    instance = MockClass.return_value
    instance.method.return_value = "result"
    
    obj = module.MyClass()
    assert obj.method() == "result"
```

### Mocking HTTP Requests

```python
@patch("requests.get")
def test_api_call(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "test"}
    mock_get.return_value = mock_response
    
    response = requests.get("https://api.example.com/users/1")
    
    assert response.status_code == 200
    assert response.json()["name"] == "test"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### Mocking File Operations

```python
@patch("builtins.open", create=True)
def test_file_read(mock_open):
    mock_open.return_value.__enter__.return_value.read.return_value = "file content"
    
    with open("file.txt") as f:
        content = f.read()
    
    assert content == "file content"
```

### Mocking Environment Variables

```python
def test_env_variable(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    
    import os
    assert os.getenv("API_KEY") == "test-key"
```

---

## Markers

### Custom Markers

```python
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow
    integration: marks integration tests
    e2e: marks end-to-end tests

# Usage in test
@pytest.mark.slow
def test_slow_operation():
    time.sleep(5)
    assert True

@pytest.mark.integration
def test_database_connection():
    # Test that requires database
    pass
```

### Running Specific Markers

```bash
# Run only tests with specific marker
pytest -m slow

# Run tests excluding a marker
pytest -m "not slow"

# Combine markers
pytest -m "integration and not slow"
```

### Skip and XFail

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8+")
def test_python38_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_known_bug():
    # Test will run but failure is expected
    assert 1 == 2
```

---

## Async Testing

### Basic Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None

@pytest.mark.asyncio
async def test_concurrent_operations():
    tasks = [fetch_data(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    assert len(results) == 10
```

### Async Fixtures

```python
@pytest.fixture
async def async_client():
    client = await create_client()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    result = await async_client.get("/api/data")
    assert result.status_code == 200
```

### Mocking Async Functions

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_mock():
    mock = AsyncMock(return_value={"data": "test"})
    
    result = await mock()
    assert result == {"data": "test"}
```

---

## Database Testing

### SQLAlchemy Testing

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create tables
    Base.metadata.create_all(engine)
    
    yield session
    
    session.close()

def test_create_user(db_session):
    user = User(name="Test", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
```

### Transaction Rollback Pattern

```python
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()
    transaction = connection.begin()
    
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def test_isolated(db_session):
    # Changes are rolled back after test
    user = User(name="Test")
    db_session.add(user)
    db_session.commit()
```

---

## API Testing

### FastAPI Testing

```python
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client():
    from main import app
    return TestClient(app)

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"name": "Test", "email": "test@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test"

def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
```

### Flask Testing

```python
import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data
```

---

## Advanced Patterns

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a

@given(st.text())
def test_string_reverse_twice(s):
    assert s == s[::-1][::-1]

@given(st.lists(st.integers()))
def test_list_length(lst):
    assert len(lst) >= 0
```

### Doctest Integration

```python
def add(a, b):
    """
    Add two numbers.
    
    >>> add(1, 2)
    3
    >>> add(-1, 1)
    0
    """
    return a + b

# pytest automatically runs doctests with --doctest-modules
```

### Test Subprocesses

```python
def test_subprocess():
    import subprocess
    result = subprocess.run(
        ["python", "-c", "print('hello')"],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "hello"
```

### Custom Assertion Helpers

```python
def assert_valid_user(user):
    assert user is not None
    assert "id" in user
    assert "email" in user
    assert "@" in user["email"]

def test_user_data():
    user = get_user(1)
    assert_valid_user(user)
```

---

## Performance Tips

### Parallel Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 workers
```

### Fast Test Discovery

```python
# Use specific test paths
pytest tests/unit/  # Only unit tests

# Use markers to filter
pytest -m "not slow"
```

### Minimize Fixture Scope

```python
# Prefer function scope over module scope
# when fixture is cheap to create
@pytest.fixture(scope="function")  # Good
def cheap_fixture():
    return {"key": "value"}

# Use module/session scope for expensive resources
@pytest.fixture(scope="session")  # Good for expensive
def expensive_resource():
    return create_expensive_resource()
```