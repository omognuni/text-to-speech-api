from fastapi import APIRouter
from app.controllers.router import audio, project

router = APIRouter(prefix='/api/v1')

router.include_router(audio.router)
router.include_router(project.router)
