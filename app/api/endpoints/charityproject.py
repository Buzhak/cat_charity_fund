from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.core import investition
from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)

from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate
)

router = APIRouter()

@router.post(
    '/',
    response_model=CharityProjectDB,
)
async def create_new_charity_project(
    new_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(new_project.name, session)
    new_charity_project = await charityproject_crud.create(
        new_project, session
    )
    await investition(session)
    await session.refresh(new_charity_project)
    return new_charity_project
    

@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charityproject_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    charity_project = await charityproject_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charityproject_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
