# Pydantic & Python Concepts Guide

This repository contains notes, definitions, and code examples covering core Pydantic features, Python unpacking, and Pytest.

## Table of Contents
1. [Pydantic `BaseModel`](#1-pydantic-basemodel)
2. [Python Dictionary Unpacking (`**`)](#2-python-dictionary-unpacking-)
3. [Custom Validators (`@field_validator` & `@classmethod`)](#3-custom-validators-field_validator--classmethod)
4. [Aliases in Pydantic (`alias` & `by_alias`)](#4-aliases-in-pydantic-alias--by_alias)
5. [Employee Model Code](#5-employee-model-code)
6. [Pytest & The `-v` Flag](#6-pytest--the--v-flag)

---

## 1. Pydantic `BaseModel`
`BaseModel` is the core class in Pydantic used to define objects that provide automatic data validation, serialization, and documentation based on Python type hints.

**Core Features:**
*   **Type Coercion:** Automatically converts compatible types (e.g., passing string `"123"` to an `int` field).
*   **Constraints with `Field`:** Used for complex validation (e.g., `Field(gt=0, min_length=3)`).
*   **V2 Methods:**
    *   `model_dump()`: Converts model to a dictionary.
    *   `model_dump_json()`: Converts model to a JSON string.
    *   `model_validate()` / `model_validate_json()`: Creates a model instance from a dict or JSON string.

## 2. Python Dictionary Unpacking (`**`)
The `**` operator is used to unpack dictionaries into key-value pairs. 
*   **Merging Dictionaries:** `config = {**defaults, **user_prefs}`
*   **Passing Arguments:** `create_user(**user_data)` (keys must match function parameters).
*   **Catching Arguments (`**kwargs`):** Bundles extra keyword arguments into a dictionary inside a function.

## 3. Custom Validators (`@field_validator` & `@classmethod`)
In Pydantic V2, `@field_validator` is used with `@classmethod` to write custom validation logic. The `@classmethod` is required because validation happens *during* object creation, before the instance (`self`) exists.

*   **Mutating Data:** Validators can transform data (e.g., returning `value.lower()`).
*   **Execution Timing:** Use `mode='before'` to run custom logic before Pydantic's internal type checking.

## 4. Aliases in Pydantic (`alias` & `by_alias`)
Used to bridge the gap between external data formats (like `camelCase` JSON) and internal Python `snake_case`.
*   **`alias`:** Defines the external name to look for during validation.
*   **`by_alias`:** A flag used during export (`model_dump(by_alias=True)`) to output the data using the defined aliases.
*   **V2 Specifics:** You can also use `validation_alias` (for reading) and `serialization_alias` (for exporting).

---

## 5. Employee Model Code
Below is the `Employee` model discussed, which enforces various constraints and includes a custom validator allowing at most one underscore in the username.

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class Employee(BaseModel):
    id: int = Field(gt=0, description="id of an employee is a positive integer")
    name: str = Field(min_length=3, description="name of the employee")
    email: EmailStr
    username: str
    age: int = Field(gt=0, lt=200, description="age of the user")
    is_manager: bool = False

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if value.count('_') > 1:
            raise ValueError("Username cannot have more than one underscore")
        
        if not value.replace('_', '').isalnum():
            raise ValueError("Username must be alphanumeric (letter, numbers and upto one underscore)")
        
        return value.lower()
```

## 5. Pytest & The -v Flag
The code above was tested using pytest.

The -v Flag: Stands for Verbose. In pytest, running pytest test_employee.py -v prints detailed information, listing every single test function by name and stating whether it PASSED or FAILED.