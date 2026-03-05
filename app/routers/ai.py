import httpx
from uuid import UUID
from typing import Annotated, List

from fastapi.routing import APIRouter
from fastapi import Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import AIRequest, AIResponse


router = APIRouter()


@router.post("", response_model=AIResponse, status_code=status.HTTP_200_OK)
async def prompt_bot(
    form_data: AIRequest, current_user: Annotated[User, Depends(get_current_user)]
):
    ollama_url = "http://host.docker.internal:11434/api/generate"
    timeout = 300.0
    async with httpx.AsyncClient(timeout=timeout) as client:
        httpx_obj = await client.post(
            ollama_url,
            json={"model": "mistral", "prompt": form_data.prompt, "stream": False},
        )
        response = httpx_obj.json()

        return {"response": response["response"]}
