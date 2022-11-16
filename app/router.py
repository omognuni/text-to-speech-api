from fastapi import APIRouter

from resources import audio, project

router = APIRouter(prefix='/api/v1')

router.include_router(project.router)
router.include_router(audio.router)
