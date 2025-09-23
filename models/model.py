from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import * # type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship,join
import bcrypt

db=SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    task1_attempts: Mapped[int] = mapped_column(Integer, default=0)
    task2_attempts: Mapped[int] = mapped_column(Integer, default=0)
    task3_attempts: Mapped[int] = mapped_column(Integer, default=0)
    
    task1_stage: Mapped[int] = mapped_column(Integer, default=1)
    task1_hint_start: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    task2_stage: Mapped[int] = mapped_column(Integer, default=1)
    task2_hint_start: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    task3_stage: Mapped[int] = mapped_column(Integer, default=1)
    task3_hint_start: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    
    def __init__(self,email,name,password,):
        self.name=name
        self.email=email
        self.password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8'))

    def set_password(self,password):
        return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')