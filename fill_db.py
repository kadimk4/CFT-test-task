from faker import Faker
from random import randint, choice


from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.auth.database import User,  sync_session_maker


db = sync_session_maker()
faker = Faker()

first_names = [faker.first_name() for _ in range(20)]
last_names = [faker.last_name() for _ in range(20)]
dates = [faker.date() for _ in range(30)]
salaries = [randint(20000, 250000) for _ in range(20)]
emails = [faker.email() for _ in range(30)]
passwords = [faker.password() for _ in range(10)]


def create_users(count: int, session: Session) -> User:
    pass_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    new_users = []
    for i in range(count):

        new_user = User(first_name=choice(first_names),
                        last_name=choice(last_names),
                        role='user',
                        hashed_password=pass_context.hash(choice(passwords)),
                        email=choice(emails),
                        salary=str(choice(salaries)), date=choice(dates))
        new_users.append(new_user)
    session.add_all(new_users)
    session.commit()


create_users(300, db)