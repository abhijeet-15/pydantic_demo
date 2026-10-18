import pytest
from pydantic import ValidationError
from index import Employee  # Replace with your actual import

def test_valid_employee():
    """Test creating an employee with valid data."""
    emp = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        username="Alice_123",
        age=30
    )
    assert emp.id == 1
    assert emp.name == "Alice"
    assert emp.email == "alice@example.com"
    # Username should be lowercased by the validator
    assert emp.username == "alice_123" 
    assert emp.age == 30
    # is_manager should default to False
    assert emp.is_manager is False

# --- ID Tests ---

def test_invalid_id_zero_or_negative():
    """Test that ID must be strictly greater than 0."""
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=0, name="Bob", email="bob@test.com", username="bob1", age=25)
    assert "Input should be greater than 0" in str(exc_info.value)

# --- Name Tests ---

def test_invalid_name_too_short():
    """Test that name must have a minimum length of 3."""
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=2, name="Bo", email="bob@test.com", username="bob2", age=25)
    assert "String should have at least 3 characters" in str(exc_info.value)

# --- Email Tests ---

def test_invalid_email_format():
    """Test that email must be a valid format."""
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=3, name="Charlie", email="not-an-email", username="charlie3", age=40)
    assert "value is not a valid email address" in str(exc_info.value)

# --- Username Tests ---

def test_username_lowercase_conversion():
    """Test that valid usernames are correctly converted to lowercase."""
    emp = Employee(id=4, name="Dave", email="dave@test.com", username="DAVE_O", age=35)
    assert emp.username == "dave_o"

def test_invalid_username_multiple_underscores():
    """Test that username rejects more than one underscore."""
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=5, name="Eve", email="eve@test.com", username="Eve__1", age=28)
    assert "Username cannot have more than one underscore" in str(exc_info.value)

def test_invalid_username_special_characters():
    """Test that username rejects spaces and non-alphanumeric characters."""
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=6, name="Frank", email="frank@test.com", username="frank space", age=45)
    assert "Username must be alphanumeric" in str(exc_info.value)
    
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=6, name="Frank", email="frank@test.com", username="frank@123", age=45)
    assert "Username must be alphanumeric" in str(exc_info.value)

# --- Age Tests ---

def test_invalid_age_out_of_bounds():
    """Test that age must be between 1 and 199 (gt=0, lt=200)."""
    with pytest.raises(ValidationError) as exc_info:
        Employee(id=7, name="Grace", email="grace@test.com", username="grace7", age=0)
    assert "Input should be greater than 0" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        Employee(id=8, name="Grace", email="grace@test.com", username="grace8", age=200)
    assert "Input should be less than 200" in str(exc_info.value)

# --- Type Coercion Tests ---

def test_type_coercion():
    """Test that Pydantic automatically converts compatible types."""
    emp = Employee(
        id="10",             # String cast to int
        name="Hank",
        email="hank@test.com",
        username="hank10",
        age="50",            # String cast to int
        is_manager="true"    # String cast to bool
    )
    assert emp.id == 10
    assert emp.age == 50
    assert emp.is_manager is True