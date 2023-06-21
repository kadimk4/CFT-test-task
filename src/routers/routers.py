from types import NoneType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.auth.database import User, get_async_session, get_sync_session
from src.auth.schemas import UserRead
from src.routers.current_users import current_user

user = APIRouter(
    prefix='/user',
    tags=['USER']
)

admin = APIRouter(
    prefix='/adminpanel',
    tags=['ADMIN']
)


class Rolecheker:
    role = ['admin']

    def __call__(self, user: User = Depends(current_user)):
        try:
            if user.role not in self.role:
                return 'make something deal'
        except:
            raise HTTPException(status_code=400,
                                detail="not enough permissions, come back when u you'll become a GIGACHAD")


allowed_roles = Rolecheker()

# user route >>>
@user.get('/information', response_model=UserRead)
async def get_info(user: User = Depends(current_user)):
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=200, detail='log in to your account')


@user.get('/salary')
async def get_salary(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        salary_ = await session.get(User, user.id)
        return f'My salary is {salary_.salary}'
    except:
        raise HTTPException(status_code=400, detail='login to your account')


# admin route >>>


@admin.get('/salary', dependencies=[Depends(allowed_roles)])
async def get_other_salary(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        salary_ = await session.get(User, user_id)
        return f'{salary_.first_name} salary is {salary_.salary}'
    except:
        raise HTTPException(status_code=400, detail='user not found, try again >:(')


@admin.get('/date', dependencies=[Depends(allowed_roles)])
async def get_other_date(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        date_ = await session.get(User, user_id)
        return f'{date_.first_name} date is {date_.date}'
    except:
        raise HTTPException(status_code=400, detail='user not found, try again >:(')

@admin.get('/user/data', dependencies=[Depends(allowed_roles)], response_model=UserRead)
async def get_user_data(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user_ = await session.get(User, user_id)
        return user_
    except:
        raise HTTPException(status_code=400, detail='user not found, try again >:(')


@admin.patch('/change/salary', dependencies=[Depends(allowed_roles)])
async def change_salary(user_id: int, new_salary: int, session: AsyncSession = Depends(get_async_session)):
    try:
        salary_ = await session.get(User, user_id)
    # if salary_ is not None:
        salary_.salary = new_salary
        await session.commit()
        return 'successful change salary'
    except:
        raise HTTPException(status_code=400, detail="has no salary")


@admin.patch('/change/date', dependencies=[Depends(allowed_roles)])
async def change_date(user_id: int, new_date: str, session: AsyncSession = Depends(get_async_session)):
    try:
        date_ = await session.get(User, user_id)
        date_.date = new_date
        await session.commit()
        return 'successful change date'
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"has no promotion date {e}")


@admin.delete('/delete', dependencies=[Depends(allowed_roles)])
def delete_data(user_id: int, session: Session = Depends(get_sync_session)):
    try:
        delete = session.query(User).where(User.id == user_id).first()
        session.delete(delete)
        session.commit()
        return 'successful deleted'
    except:
        raise HTTPException(status_code=400, detail="user not found, try again >:(")