from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    pass
    
    

class DonationCreate(DonationBase):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


# class DonationUpdate(BaseModel):
#     comment: Optional[str]


class DonationShortDB(DonationBase):
    comment: Optional[str]
    create_date: datetime
    full_amount: int
    id: int

    class Config:
        orm_mode = True

class DonationFullDB(DonationBase):
    comment: Optional[str]
    create_date: datetime
    full_amount: int
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True
