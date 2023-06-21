from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.database import User
from src.auth.manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_admin = fastapi_users.current_user(role='admin')