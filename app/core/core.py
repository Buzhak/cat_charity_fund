from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.charityproject import Charityproject
from app.models.donation import Donation


async def get_not_full_investition_list(
    model: Charityproject or Donation, session: AsyncSession
) -> (
    list[Charityproject,] or list[Donation,]
):
    '''Функция отдаёт все оъекты, средства в коротых не были распределены до конца'''
    not_fully_invested = await session.execute(
            select(model).where(
                model.fully_invested == False
            )
        )
    not_fully_invested = not_fully_invested.scalars().all()
    return not_fully_invested


async def update_data_in_db(donation_db: Donation, project_db: Charityproject, session: AsyncSession) -> None:
    '''Обновляем данные в ДБ'''
    session.add(donation_db)
    session.add(project_db)
    await session.commit()
    await session.refresh(donation_db)
    await session.refresh(project_db)


async def close_bd_obj(obj_db: Donation or Charityproject) -> Donation or Charityproject:
    '''
    Закрываем запись в БД
    Ставим "invested_amount" равным "full_amount"
    "fully_invested" = True
    и ставис текущее время в "close_date"     
    '''
    obj_db.invested_amount = obj_db.full_amount
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db


async def investition(session: AsyncSession) -> None:
    not_fully_invested_projects = await get_not_full_investition_list(Charityproject, session)
    # not_fully_invested_donations = await get_not_full_investition_list(Donation, session)

    if len(not_fully_invested_projects) != 0:
        for project_db in not_fully_invested_projects:
            not_fully_invested_donations = await get_not_full_investition_list(Donation, session)
            for donation_db in not_fully_invested_donations:
                project_amount = project_db.full_amount - project_db.invested_amount
                donation_amount = donation_db.full_amount - donation_db.invested_amount
                if project_amount == 0:
                    break
                if project_amount == donation_amount:
                    donation_db = await close_bd_obj(donation_db)
                    project_db = await close_bd_obj(project_db)
                    await update_data_in_db(donation_db, project_db, session)

                elif project_amount > donation_amount:
                    donation_db = await close_bd_obj(donation_db)
                    project_db.invested_amount = project_db.invested_amount + donation_db.full_amount
                    await update_data_in_db(donation_db, project_db, session)

                # elif project_amount < donation_amount:
                else:
                    donation_db.invested_amount = project_amount
                    project_db = await close_bd_obj(project_db)
                    await update_data_in_db(donation_db, project_db, session)
