from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]
    

class DonationCreate(DonationBase):
    pass

class DonationUpdate(BaseModel):
    comment: Optional[str]

class DonationShortDB(DonationBase):

    class Config:
        orm_mode = True

class DonationFullDB(DonationBase):

    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: datetime

    class Config:
        orm_mode = True
