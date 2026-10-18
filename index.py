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
