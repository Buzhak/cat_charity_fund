from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, validates

from app.core.db import Base
from app.models.donation import Donation

from app.models.core_models import same_time
from app.models.error_hendlers import len_not_null, int_not_zero


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, default=same_time)
     
    @validates(name, description)
    def validate_len(self, key, value):
        return len_not_null(key, value)
    
    @validates(full_amount)
    def validate_full_amount(self, key, value):
        return int_not_zero(key, value)
