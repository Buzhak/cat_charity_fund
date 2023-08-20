from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_name = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_name is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует',
        )

        
async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    meeting_room = await charity_project_crud.get(project_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден'
        )
    return meeting_room


async def check_amount(obj_db_amount: int, new_amount: int) -> None:
    if obj_db_amount > new_amount:
        raise HTTPException(
            status_code=403,
            detail=f'Сумма средств должна быть больше изначальной {obj_db_amount}',
        )


async def check_delete(obj_db_invested_amount: int) -> None:
    if obj_db_invested_amount != 0:
        raise HTTPException(
            status_code=403,
            detail=f'Нельзя удалить проект с внесёнными стредствами',
        )
