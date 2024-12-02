from fastapi import APIRouter, Depends

pictures_router = APIRouter(
    prefix="/Pictures",
    tags=["Pictures"]
)