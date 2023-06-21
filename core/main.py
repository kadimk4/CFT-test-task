from fastapi import FastAPI, Depends

from src.auth.auth import auth_backend

from src.auth.schemas import UserRead, UserCreate
from src.routers.current_users import fastapi_users, current_admin
from src.routers.routers import user, admin

app = FastAPI(
    title='testTask'
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(user)
app.include_router(admin, dependencies=[Depends(current_admin)])
