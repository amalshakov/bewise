from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Application


async def create_application(
    user_name: str,
    description: str,
    session: AsyncSession,
) -> Application:
    """
    Creates a new application and saves it to the database.
    """
    new_application = Application(
        user_name=user_name,
        description=description,
    )
    session.add(new_application)
    await session.commit()
    await session.refresh(new_application)

    return new_application


async def get_list_applications(
    user_name: Optional[str],
    page: int,
    size: int,
    session: AsyncSession,
) -> list[Application]:
    """
    Fetches a paginated list of applications, optionally filtered by user_name.
    """
    stmt = select(Application)
    if user_name:
        stmt = stmt.where(Application.user_name == user_name)
    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await session.execute(stmt)

    return list(result.scalars().all())
