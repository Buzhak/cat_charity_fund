from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import validates

from app.core.db import Base
from app.models.core_models import same_time
from app.models.error_hendlers import int_not_zero


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, default=same_time)

    
    @validates(full_amount)
    def validate_full_amount(self, key, value):
        return int_not_zero(key, value)
