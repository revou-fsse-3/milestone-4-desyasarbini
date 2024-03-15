from models.base import Base
from sqlalchemy import Integer, String, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.models.accounts import Accounts

class Transactions(Base):
    __tablename__ = 'transactions'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    amount = mapped_column(DECIMAL(precision=10, scale=2))
    type = mapped_column(String(191), nullable= False)
    description = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationship ke model accounts u/ from_account
    from_account = relationship("Accounts", foreign_keys=[from_account_id])

    # relationship ke model accounts u/ to_account
    to_account = relationship("Accounts", foreign_keys=[to_account_id])

    def __repr__(self):
        return f'<Transactions {self.type}>'