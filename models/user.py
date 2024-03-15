from models.base import Base
from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.sql import func
from flask_login import UserMixin
import 

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(191), nullable=False, unique=True)
    email = mapped_column(String(191), nullable=False, unque=True)
    password = mapped_column(String(191), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<User{self.username}>'

    # u/ encrypt password
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # u/ check password yg ter-encrypt
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
