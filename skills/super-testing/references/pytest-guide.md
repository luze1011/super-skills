# Pytest Comprehensive Guide

## Installation

```bash
pip install pytest pytest-cov pytest-xdist pytest-asyncio pytest-mock
```

## Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
asyncio_mode = auto
```

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

## Test Discovery

Pytest automatically discovers tests that match:
- Files named `test_*.py` or `*_test.py`
- Classes starting with `Test`
- Functions starting with `test_`

## Fixtures Deep Dive

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default, created for each test
def fresh_data():
    return {"id": 1}

@pytest.fixture(scope="class")  # Created once per test class
def class_data():
    return {"shared": "within class"}

@pytest.fixture(scope="module")  # Created once per module
def module_data():
    return {"shared": "within module"}

@pytest.fixture(scope="session")  # Created once per session
def session_data():
    return {"shared": "across all tests"}
```

### Fixture Dependencies

```python
@pytest.fixture
def database():
    db = Database()
    yield db
    db.close()

@pytest.fixture
def user(database):
    user = database.create_user("test@example.com")
    yield user
    database.delete_user(user.id)

def test_user_exists(user):
    assert user.email == "test@example.com"
```

### Fixture with autouse

```python
@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup: runs before each test
    print("Setup")
    yield
    # Teardown: runs after each test
    print("Teardown")
```

### conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture
def shared_fixture():
    """Available to all tests in this directory."""
    return "shared data"

@pytest.fixture
def api_client():
    from myapp.client import APIClient
    return APIClient(base_url="http://localhost:8000")
```

## Parametrization

### Basic Parametrize

```python
@pytest.mark.parametrize("value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
], ids=["one", "two", "three"])
def test_double(value, expected):
    assert value * 2 == expected
```

### Parametrize with Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres"])
def database(request):
    db = create_database(request.param)
    yield db
    db.close()

def test_database_operations(database):
    assert database.is_connected()
```

### Mixed Parametrization

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    assert x * y == x * y  # 4 test cases: (1,10), (1,20), (2,10), (2,20)
```

## Markers

### Custom Markers

```python
# Register in pytest.ini or pyproject.toml
[pytest]
markers = slow: marks tests as slow

# Usage
@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(10)
    assert True
```

### Built-in Markers

```python
@pytest.mark.skip(reason="Not ready yet")
def test_future():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

@pytest.mark.xfail(reason="Known issue #123")
def test_known_bug():
    assert False  # Will be reported as XFAIL, not FAILED

@pytest.mark.usefixtures("setup_db")
class TestDatabase:
    def test_query(self):
        pass
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result == expected

@pytest.fixture
async def async_setup():
    data = await load_data()
    yield data
    await cleanup_data()
```

## Mocking

### Using pytest-mock

```python
def test_with_mocker(mocker):
    # Mock a function
    mocker.patch('module.function', return_value=42)
    assert module.function() == 42
    
    # Mock an object method
    obj = SomeClass()
    mocker.patch.object(obj, 'method', return_value='mocked')
    assert obj.method() == 'mocked'
    
    # Spy on a function (calls original)
    spy = mocker.spy(module, 'function')
    module.function(1, 2)
    spy.assert_called_once_with(1, 2)
```

### Using unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

@patch('module.api_call')
def test_api(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = module.api_call()
    assert result["status"] == "ok"

def test_mock_class():
    mock_obj = MagicMock()
    mock_obj.method.return_value = "mocked"
    assert mock_obj.method() == "mocked"
```

## Coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=term --cov-report=html

# Coverage configuration in .coveragerc
[run]
source = src
omit = */tests/*

[report]
exclude_lines =
    pragma: no cover
    if TYPE_CHECKING:
    raise NotImplementedError
fail_under = 80
```

## Parallel Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto  # Use all CPUs
pytest -n 4     # Use 4 workers

# Load balancing
pytest --dist=loadscope  # Group by module/class
pytest --dist=each       # Run on all workers
```

## Debugging

```bash
# Enter debugger on failure
pytest --pdb

# Enter debugger at start
pytest --trace

# Show local variables in traceback
pytest -l

# Verbose output
pytest -vv

# Print statements in tests
pytest -s
```

## Best Practices

1. **Name tests descriptively**
   ```python
   def test_user_registration_sends_email():
       pass
   ```

2. **One assertion concept per test**
   ```python
   # Good
   def test_user_creation():
       user = create_user("test@example.com")
       assert user.id is not None
   
   def test_user_email():
       user = create_user("test@example.com")
       assert user.email == "test@example.com"
   ```

3. **Use fixtures for setup/teardown**
   ```python
   @pytest.fixture
   def clean_database():
       db = Database()
       yield db
       db.truncate_all()
   ```

4. **Keep tests independent**
   ```python
   # Bad: depends on test_create_user running first
   def test_delete_user():
       delete_user(user_id)
   
   # Good: creates its own data
   def test_delete_user():
       user = create_user("delete@test.com")
       delete_user(user.id)
   ```

5. **Use parametrize for similar tests**
   ```python
   @pytest.mark.parametrize("email,valid", [
       ("test@example.com", True),
       ("invalid", False),
       ("@nodomain.com", False),
   ])
   def test_email_validation(email, valid):
       assert validate_email(email) == valid
   ```