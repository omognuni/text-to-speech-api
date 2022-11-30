from audio.endpoints import router as audio
from fastapi import APIRouter

router = APIRouter(prefix='/api/v1')

router.include_router(audio)