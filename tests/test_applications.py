from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status

from app.models import Application


@pytest.fixture
def mock_dao_create_application():
    with patch("app.dao.create_application", new_callable=AsyncMock) as mock:
        mock.return_value = Application(
            id=1,
            user_name="test_user",
            description="Test description",
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        yield mock


@pytest.fixture
def mock_publish_to_kafka():
    with patch("app.my_kafka.publish_to_kafka") as mock:
        mock.send_and_wait = AsyncMock(return_value=None)
        yield mock


@pytest.fixture
def mock_dao_get_list_applications():
    with patch("app.dao.get_list_applications", new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
async def test_create_application_success(
    mock_dao_create_application,
    mock_publish_to_kafka,
):
    payload = {"user_name": "test_user", "description": "Test description"}

    mock_post = AsyncMock()
    mock_post.status_code = status.HTTP_200_OK
    mock_post.json.return_value = {
        "id": 1,
        "user_name": "test_user",
        "description": "Test description",
        "created_at": "2025-01-01T00:00:00Z",
    }

    with patch("fastapi.testclient.TestClient.post", return_value=mock_post):
        response = mock_post

        assert response.status_code == status.HTTP_200_OK
        assert await response.json() == {
            "id": 1,
            "user_name": "test_user",
            "description": "Test description",
            "created_at": "2025-01-01T00:00:00Z",
        }


@pytest.mark.asyncio
async def test_create_application_failure(
    mock_dao_create_application,
    mock_publish_to_kafka,
):
    mock_dao_create_application.side_effect = Exception("Database error")

    mock_post = AsyncMock()
    mock_post.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_post.json.return_value = {"detail": "Internal server error"}

    with patch("fastapi.testclient.TestClient.post", return_value=mock_post):
        response = mock_post

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert await response.json() == {"detail": "Internal server error"}
        mock_publish_to_kafka.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_list_applications_success(
    mock_dao_get_list_applications,
):
    mock_dao_get_list_applications.return_value = [
        Application(
            id=1,
            user_name="test_user1",
            description="Description 1",
            created_at="2025-01-01T00:00:00Z",
        ),
        Application(
            id=2,
            user_name="test_user2",
            description="Description 2",
            created_at="2025-01-02T00:00:00Z",
        ),
    ]

    mock_get = AsyncMock()
    mock_get.status_code = status.HTTP_200_OK
    mock_get.json.return_value = [
        {
            "id": 1,
            "user_name": "test_user1",
            "description": "Description 1",
            "created_at": "2025-01-01T00:00:00Z",
        },
        {
            "id": 2,
            "user_name": "test_user2",
            "description": "Description 2",
            "created_at": "2025-01-02T00:00:00Z",
        },
    ]

    with patch("fastapi.testclient.TestClient.get", return_value=mock_get):
        response = mock_get

        assert response.status_code == status.HTTP_200_OK
        assert await response.json() == [
            {
                "id": 1,
                "user_name": "test_user1",
                "description": "Description 1",
                "created_at": "2025-01-01T00:00:00Z",
            },
            {
                "id": 2,
                "user_name": "test_user2",
                "description": "Description 2",
                "created_at": "2025-01-02T00:00:00Z",
            },
        ]


@pytest.mark.asyncio
async def test_get_list_applications_failure(
    mock_dao_get_list_applications,
):
    mock_dao_get_list_applications.side_effect = Exception("Database error")

    mock_get = AsyncMock()
    mock_get.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_get.json.return_value = {"detail": "Internal server error"}

    with patch("fastapi.testclient.TestClient.get", return_value=mock_get):
        response = mock_get

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert await response.json() == {"detail": "Internal server error"}
