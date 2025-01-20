from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import dao
from app.database import get_session
from app.logger import get_logger
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationResponse
from app.my_kafka import publish_to_kafka

router = APIRouter()

logger = get_logger()


@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    session: AsyncSession = Depends(get_session),
) -> Application:
    """
    Creates a new application for the specified user.

    The application is saved to the database and a message
    is published to Kafka for further processing.
    """
    logger.info(
        f"Received request to create a new application for user "
        f"{application.user_name!r}"
    )
    try:
        new_application = await dao.create_application(
            user_name=application.user_name,
            description=application.description,
            session=session,
        )
        await publish_to_kafka(new_application)
        logger.info(
            f"Successfully created application with ID: {new_application.id}"
        )
        return new_application

    except Exception as error:
        logger.error(
            f"Error while creating application for user "
            f"{application.user_name!r}: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=list[ApplicationResponse])
async def get_list_applications(
    user_name: str = Query(None),
    page: int = 1,
    size: int = 10,
    session: AsyncSession = Depends(get_session),
) -> list[Application]:
    """
    Retrieves a list of applications with optional filtering and pagination.
    """
    logger.info(
        f"Received request to list applications. "
        f"(user_name={user_name!r}, page={page}, size={size})"
    )
    try:
        applications = await dao.get_list_applications(
            user_name=user_name,
            page=page,
            size=size,
            session=session,
        )
        logger.info(
            f"Successfully retrieved {len(applications)} application(s)"
        )
        return applications

    except Exception as error:
        logger.error(f"Error while listing applications: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
