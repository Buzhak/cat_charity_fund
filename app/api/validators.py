# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models.charityproject import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_name = await charityproject_crud.get_project_id_by_name(project_name, session)
    if project_name is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует',
        )

        
async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    meeting_room = await charityproject_crud.get(project_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден'
        )
    return meeting_room


# async def check_reservation_before_edit(
#     reservation_id: int,
#     session: AsyncSession,
#     user: User,
# ) -> Reservation:
    
#     reservation = await reservation_crud.get(
#         obj_id=reservation_id, session=session 
#     )
#     if reservation is None:
#         raise HTTPException(
#             status_code=404,
#             detail='Бронь не найдена!'
#         )
#     if not user.is_superuser or reservation.user_id != user.id:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     return reservation

# async def check_reservation_intersections(**kwargs) -> None:
#     reservation = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservation:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservation)
#         )
