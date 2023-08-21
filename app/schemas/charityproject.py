from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description')
    def check_str(cls, value):
        if len(''.join(value.split())) == 0:
            raise ValueError(
                'Поле не может стостоять из пробелов'
            )
        return value


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectShortDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True



class CharityProjectDB(BaseModel):
    create_date: datetime
    description: str
    full_amount: int
    fully_invested: bool
    id: int
    invested_amount: int
    name: str

    class Config:
        orm_mode = True
