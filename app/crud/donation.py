from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession
    ):
        select_stmt = select(Donation).where(
            Donation.user_id == user.id
        )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations
    

donation_crud = CRUDDonation(Donation)
