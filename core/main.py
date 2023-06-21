from fastapi import FastAPI, Depends, HTTPException

from src.auth.auth import auth_backend
from src.auth.database import User

from src.auth.schemas import UserRead, UserCreate
from src.routers.current_users import fastapi_users, current_admin, current_user
from src.routers.routers import user, admin

app = FastAPI(
    title='testTask'
)

@app.patch('/get_admin')
def admin_role(key: str, user: User = Depends(current_user)):
    try:
        if key == 'cft-test-case':
            user.role = 'admin'
            return 'successful given admin'
        else:
            raise HTTPException(status_code=400, detail="try again >:)")
    except:
        raise HTTPException(status_code=400, detail="mb u need login to account?")

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
