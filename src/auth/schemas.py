from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    role: str
    date: str
    salary: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
