from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessagesRepository
from app.repositories.users import UsersRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UsersRepository:
    return UsersRepository(session)


def get_chat_messages_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ChatMessagesRepository:
    return ChatMessagesRepository(session)


def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()


def get_auth_usecase(
    users_repository: UsersRepository = Depends(get_users_repository),
) -> AuthUseCase:
    return AuthUseCase(users_repository)


def get_chat_usecase(
    chat_messages_repository: ChatMessagesRepository = Depends(get_chat_messages_repository),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    return ChatUseCase(chat_messages_repository, openrouter_client)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError) as error:
        raise unauthorized_exception from error

    return user_id
