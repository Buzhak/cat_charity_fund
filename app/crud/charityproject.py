from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charityproject import Charityproject


class CRUDCharityproject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(Charityproject.id).where(
                Charityproject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

charityproject_crud = CRUDCharityproject(Charityproject)
